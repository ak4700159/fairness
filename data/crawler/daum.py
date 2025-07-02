import requests # requests패키지
import pandas as pd # pandas패키지
from bs4 import BeautifulSoup # BeautifulSoup패키지

# 크롤링할 페이지 수, 카테고리, 날짜
def make_urllist(page_num, code, date): 
  urllist= []

  # 1 ~ page_num까지 정해진 페이지만큼 반복.
  for i in range(1, page_num + 1):

        # 함수의 입력으로 된 변수들로 주소를 조합
    url = 'https://news.daum.net/breakingnews/'+code+'?page='+str(i)+'&regDate='+str(date)

        # requets 패키지의 모듈(함수)을 호출
    news = requests.get(url)
    news.content

    # BeautifulSoup 모듈을 사용하여 HTML 페이지를 분석
    soup = BeautifulSoup(news.content, 'html.parser')

    # select로 각 뉴스의 HTML코드를 리스트로 저장
    news_list = soup.select('.list_allnews li div strong')

    # 각 뉴스의 a 태그 <a href ='주소'> 에서 '주소'만 추출
    # urllist에 저장
    for line in news_list:
        urllist.append(line.a.get('href'))
  return urllist


if __name__ == "__main__":
   url_list = make_urllist(2, 'society', 20250103) 
   print('뉴스 기사의 개수 :',len(url_list))