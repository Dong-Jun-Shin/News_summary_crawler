# News summary crawler
- 네이버 뉴스의 기사 중 'IT과학', '경제', '사회' 분야의 기사 20개씩 가져와서 요약 후 md 파일로 생성
- 카테고리 별로 'output/{날짜}/Article_{카테고리}_{날짜}.md' 파일 생성
- 'output' 폴더에 최근 30일까지 뉴스에 한해, 날짜별로 보관
- 매일 오후 3시에 업로드(한국 시간)

___

### 폴더 구조

- output : 요약된 뉴스 폴더(.md)  
- src : 크롤러 소스 코드(.py)  

___

### 뉴스 기사 마크다운 템플릿
<br/>
<pre>
  <br/>
  <!-- 타이틀 -->
  # {text_headline}
  <!-- 기사 정보 -->
  > Date : {time}  
  > Author : {text_company}  
  > Original : [원문기사]({content_url})  
  <br/>
  <!-- 대표 이미지 -->
  {img_content}
  <br/><br/>
  <!-- 기사 본문 -->
  {text_sentence}
  <br/><br/><br/>
</pre>

___

### 산출물 (모바일)  
- 폴더 및 뉴스 샘플  
![폴더 샘플](https://github.com/Dong-Jun-Shin/News_summary_crawler/blob/main/read_me_img/1.jpg)  
![뉴스 샘플](https://github.com/Dong-Jun-Shin/News_summary_crawler/blob/main/read_me_img/2.jpg)  
<br/><br/>
### 산출물 (데스크톱)  
![폴더 샘플](https://github.com/Dong-Jun-Shin/News_summary_crawler/blob/main/read_me_img/3.png)  
<img src="https://github.com/Dong-Jun-Shin/News_summary_crawler/blob/main/read_me_img/4.png" style="width:100%"/><br/>
<img src="https://github.com/Dong-Jun-Shin/News_summary_crawler/blob/main/read_me_img/5.png" style="width:100%"/><br/>
<br/><br/>

___

### 참고 소스
- Crawler Source [lumyjuwon/KoreaNewsCrawler](https://github.com/lumyjuwon/KoreaNewsCrawler)
- Github Actions Cron Source [zzsza/github-action-with-python](https://github.com/zzsza/github-action-with-python)
