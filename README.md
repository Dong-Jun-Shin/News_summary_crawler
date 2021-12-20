# News_crawler
- 네이버 뉴스의 기사 중 'IT과학', '경제', '사회' 분야의 기사 20개씩 가져와서 md 파일로 표시
- 카테고리 별로 '{날짜}/Article_{카테고리}_{날짜}.md' 파일 생성

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
- [lumyjuwon/KoreaNewsCrawler](https://github.com/lumyjuwon/KoreaNewsCrawler)
