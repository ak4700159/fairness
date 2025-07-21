from selenium.webdriver.common.by import By
from crawler.crawler import Crawler 
from article import Article as DataArticle
from newspaper import Article as NewsArticle
import time
import re

# https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=indices
class NaverCrawler(Crawler):
    def collect_article_links(self):
        try:
            # 기사 리스트 페이지 열기
            base_url = f"https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query={self.keyword}"
            self.driver.get(base_url)
        except:
            # 재시도
            self.driver.get(base_url)
            time.sleep(1.5)
        total_links = set()
        # 기사링크 수집
        for i in range(self.max_pages):
            # 태그 + 클래스 속성을 통해 HTML 태그를 전부 선택
            articles = self.driver.find_elements(By.CSS_SELECTOR, "a.OqRuWgaJW9JVSHu5Dl92.BAeT2rSB_v3C8l_Lu2U6")
            # {"page" : 페이지 인덱스, "links" : [링크 목록]}
            links = {"page" : i+1, "links" : []}
            # 선택된 태그의 속성(href)을 통해 기사 원본 링크 주소 추출
            # HTML 코드 상단에서부터 추출되기에 인덱스 0은 맨 위에 노출된 기사가 된다.
            for article in articles:
                try:
                    href = article.get_attribute("href")
                    if href and (href not in total_links):
                        total_links.add(href)
                        links['links'].append(href)
                except:
                    continue
            self.article_links.append(links)
            print(f"{i+1}페이지 링크 리스트({len(links['links'])}개) : \n{links}")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)

    # 기사제목과 원본 추출
    def extract_article_data(self, url, index, page):
        article = NewsArticle(url=url, language='ko')
        try:
            article.download()
            article.parse()
            title = article.title
            content = article.text  
            datetime_obj = article.publish_date
            datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S") if datetime_obj else ""        
        except:
            return None
        # 크롤링된 기사 본문 개행 문자 수정
        content = re.sub(r'\n{2,}', '\n', content) 
        content = content.lstrip('\n')
        print(f"✅ 수집 완료: {title[:20]}... / {content[:20]}...")
        return DataArticle(**{
            "title": title, 
            "content": content, 
            "datetime" : datetime_str,
            "url" : url, 
            "index" : index+1, 
            "page" : page, 
            "keyword" : self.keyword,
            "site" : self.site,
        })

if __name__ == "__main__":
    crawler = NaverCrawler(keyword="민생지원 정책", site="naver")
    crawler.run()