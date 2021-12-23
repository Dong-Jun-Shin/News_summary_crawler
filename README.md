# News summary crawler
- 네이버 뉴스의 기사 중 'IT과학', '경제', '사회' 분야의 기사 20개씩 가져와서 요약 후 md 파일로 생성
- 카테고리 별로 'output/{날짜}/Article_{카테고리}_{날짜}.md' 파일 생성
- 'output' 폴더에 최근 한 달까지의 뉴스만 날짜별로 보관
- 매일 오후 6시에 업로드(한국 시간)

___

### 폴더 구조

- output : 요약된 뉴스 폴더(.md)  
- src : 크롤러 소스 코드(.py)  

___

### 뉴스 기사 템플릿
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

### 참고 소스
- Crawler Source [lumyjuwon/KoreaNewsCrawler](https://github.com/lumyjuwon/KoreaNewsCrawler)
- Github Actions Cron Source [zzsza/github-action-with-python](https://github.com/zzsza/github-action-with-python)
