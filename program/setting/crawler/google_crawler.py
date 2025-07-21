from crawler.crawler import Crawler 
from selenium.webdriver.common.by import By
from article import Article as DataArticle
from newspaper import Article as NewsArticle
import time
import re

# https://www.google.com/search?sca_esv=ac35dc61bdce8476&biw=923&bih=911&sxsrf=AE3TifPoxiFlTNLi_uCJQPrs9rsK3h9zjQ:1752853385937&q={검색내용}&start={검색페이지 0(1페이지) 10(2페이지) 20(3페이지) .. 단위}&tbm=nws&source=lnms&fbs=AIIjpHyDg0Pef0CibV20xjIa-FRejxCuOmkq074km2sZXr7uqz9_8tiStZcoMiP-q5iAtTZL8-ZdTewwQWlWih-7esbNqLyFsX9fEY6BUkpv7Mr3vy10-lHh67LQwmG5NF0mShSfA6dOHL5998caaqXb3B7MKmb2KnWis_dyzp2-ySRhUdM-QXO8trHsUAL13A5M9RN2htuoIk_V5e5_I1gizgT5CX6MEQ&sa=X&ved=2ahUKEwil6qXb38aOAxWNzTQHHSgvFpAQ0pQJKAN6BAgQEAE
class GoogleCrawler(Crawler):
    def collect_article_links(self):
        # 기사링크 수집
        for i in range(self.max_pages):
            try:
                # 기사 리스트 페이지 열기
                base_url = f"https://www.google.com/search?q={self.keyword}&sca_esv=1dbd1f19de3e7c2c&tbm=nws&ei=jP96aOakF7G7vr0Pru-0iQE&start={i * 10}&sa=N&ved=2ahUKEwjmmu_u7MeOAxWxna8BHa43LREQ8tMDegQIBRAE&biw=1920&bih=911&dpr=1"
                self.driver.get(base_url)
                time.sleep(1.5)
            except:
                # 재시도
                self.driver.get(base_url)
                time.sleep(1.5)

            # 태그 + 클래스 속성을 통해 HTML 태그를 전부 선택
            articles = self.driver.find_elements(By.CSS_SELECTOR, "a.WlydOe")
            # {"page" : 페이지 인덱스, "links" : [링크 목록]}
            links = {"page" : i+1, "links" : []}
            # 선택된 태그의 속성(href)을 통해 기사 원본 링크 주소 추출
            # HTML 코드 상단에서부터 추출되기에 인덱스 0은 맨 위에 노출된 기사가 된다.
            for article in articles:
                try:
                    href = article.get_attribute("href")
                    if href:
                        links['links'].append(href)
                except:
                    continue
            self.article_links.append(links)
            print(f"{i+1}페이지 링크 리스트({len(links['links'])}개) : \n{links}")

    # 기사제목과 원본 추출
    def extract_article_data(self, url, index, page):
        article = NewsArticle(url=url, language='ko')
        try:
            article.download()
            article.parse()
            title = article.title
            content = article.text  
            datetime = article.publish_date
        except:
            return None
        # 크롤링된 기사 본문 개행 문자 수정
        content = re.sub(r'\n{2,}', '\n', content) 
        content = content.lstrip('\n')
        print(f"✅ 수집 완료: {title[:20]}... / {content[:20]}...")
        return DataArticle(**{
            "title": title, 
            "content": content, 
            "datetime" : datetime,
            "url" : url, 
            "index" : index+1, 
            "page" : page, 
            "keyword" : self.keyword,
            "site" : self.site,
        })

if __name__ == "__main__":
    crawler = GoogleCrawler(keyword="민생지원 정책", site="구글")
    crawler.run()