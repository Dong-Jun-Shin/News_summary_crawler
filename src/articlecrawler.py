#!/usr/bin/env python
# -*- coding: utf-8, euc-kr -*-

import os
import platform
import requests
import re
from datetime import date
from time import sleep
from bs4 import BeautifulSoup
from exceptions import *
from articleparser import ArticleParser
from writer import Writer
from gensim.summarization.summarizer import summarize


class ArticleCrawler(object):
    def __init__(self):
        self.categories = {'정치': 100, '경제': 101, '사회': 102, '생활문화': 103, '세계': 104, 'IT과학': 105, '오피니언': 110,
                           'politics': 100, 'economy': 101, 'society': 102, 'living_culture': 103, 'world': 104, 'IT_science': 105, 'opinion': 110}
        self.selected_categories = []
        self.user_operating_system = str(platform.system())

    def set_category(self, *args):
        for key in args:
            if self.categories.get(key) is None:
                raise InvalidCategory(key)
        self.selected_categories = args

    @staticmethod
    def get_url_data(url, max_tries=5):
        remaining_tries = int(max_tries)
        while remaining_tries > 0:
            try:
                return requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
            except requests.exceptions:
                sleep(1)
            remaining_tries = remaining_tries - 1
        raise ResponseTimeout()

    def crawling(self, category_name):
        # Multi Process PID
        print(category_name + " PID: " + str(os.getpid()))

        today = date.today()
        writer = Writer(category='Article', article_category=category_name, today=today)
        # 기사 url 형식
        url_format = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={self.categories.get(category_name)}&date={str(today.year) + str(today.month) + str(today.day)}'
        target_urls = url_format

        print(category_name + " Urls are generated")
        print("The crawler starts")

        request = self.get_url_data(target_urls)
        document = BeautifulSoup(request.content, 'html.parser')

        # html - newsflash_body - type06_headline, type06
        # 각 페이지에 있는 기사들 가져오기
        temp_post = document.select('.newsflash_body .type06_headline li dl')
        temp_post.extend(document.select('.newsflash_body .type06 li dl'))

        # 각 페이지에 있는 기사들의 url 저장
        post_urls = []
        for line in temp_post:
            # 해당되는 page에서 모든 기사들의 URL을 post_urls 리스트에 넣음
            post_urls.append(line.a.get('href'))
        del temp_post

        for content_url in post_urls:  # 기사 url
            # 크롤링 대기 시간
            sleep(0.01)

            # 기사 HTML 가져옴
            request_content = self.get_url_data(content_url)

            try:
                document_content = BeautifulSoup(request_content.content, 'html.parser')
            except Exception:
                continue

            try:
                # 기사 제목 가져옴
                tag_headline = document_content.find_all('h3', {'id': 'articleTitle'}, {'class': 'tts_head'})
                # 스포츠 기사 대응 코드
                if not tag_headline:
                    tag_headline = document_content.find_all('h4', {'class': 'title'})

                # 뉴스 기사 제목 초기화
                text_headline = ''
                text_headline = text_headline + ArticleParser.clear_headline(str(tag_headline[0].find_all(text=True)))
                # 공백일 경우 기사 제외 처리
                if not text_headline:
                    continue

                # 기사 본문 가져옴
                tag_content = document_content.find_all('div', {'id': 'articleBodyContents'})
                # 스포츠 기사 대응 코드
                if not tag_content:
                    tag_content = document_content.find_all('div', {'id': 'newsEndContents'})
                # 뉴스 기사 본문 초기화
                text_sentence = ''
                text_sentence = text_sentence + ArticleParser.clear_content(str(tag_content[0].find_all(text=True)))
                # 기사 내용을 원문의 30% 비율로 요약
                try:
                    summary_contents = summarize(text_sentence, ratio=0.3)
                except Exception:
                    summary_contents = None
                # 원문의 길이가 10문장 이하 시, 앞에 3줄로 대체
                if not summary_contents:
                    orig_contents = text_sentence.split('.')
                    if len(orig_contents) > 3:
                        summary_contents = '.'.join(orig_contents[:3])
                    else:
                        summary_contents = '.'.join(orig_contents)

                # 본문 이미지
                img_content = document_content.find_all('span', {'class': 'end_photo_org'})
                # 사진 대신 동영상일 경우, 대응 코드
                if not img_content:
                    img_content = ['No Image']
                else:
                    img_content = img_content[0].contents
                img_content = str(img_content[0])

                # 공백일 경우 기사 제외 처리
                if not summary_contents:
                    continue

                # 기사 언론사 가져옴
                tag_company = document_content.find_all('meta', {'property': 'me2:category1'})
                if not tag_company:
                    tag_company = document_content.find_all('meta', {'property': 'og:article:author'})

                # 언론사 초기화
                text_company = ''
                text_company = text_company + str(tag_company[0].get('content'))
                # 스포츠 기사 대응 코드
                if not text_company.find('네이버 스포츠 | '):
                    text_company = text_company.replace('네이버 스포츠 | ', '')

                # 공백일 경우 기사 제외 처리
                if not text_company:
                    continue

                # 기사 시간대 가져옴
                time = re.findall('<span class="t11">(.*)</span>', request_content.text)
                # 스포츠 기사 대응 코드
                if not time:
                    time = re.findall('<span class="bar">(.*)</span>', request_content.text)
                time = time[0].replace("최종수정 ", "").replace("</span>", "")

                # MD 작성
                writer.write_title(text_headline)
                writer.write_info(time, text_company, content_url)
                writer.write_img(img_content)
                writer.write_sentence(summary_contents)

                del time
                del text_company, text_sentence, summary_contents, text_headline
                del tag_company
                del tag_content, tag_headline
                del request_content, document_content

            # UnicodeEncodeError
            except Exception as ex:
                del request_content, document_content
                pass
        writer.close()

    def start(self):
        # MultiProcess 크롤링 시작
        for category_name in self.selected_categories:
            self.crawling(category_name,)