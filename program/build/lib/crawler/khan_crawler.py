from selenium.webdriver.common.by import By
import time
import re
from crawler import Crawler
from article import Article as DataArticle

# https://search.khan.co.kr/?q=검색 키워드&media=khan&page=1&section=1&term=0&startDate=&endDate=&sort=1
# 필요한 데이터 = 기사제목, 기사본문

class KhanCrawler(Crawler):
    # 기사링크 수집
    def collect_article_links(self):
        for i in range(self.max_pages):
            base_url = f"https://search.khan.co.kr/?q={self.keyword}&media=khan&page={i+1}&section=1&term=0&startDate=&endDate=&sort=1"
            print(base_url)
            self.driver.get(base_url)
            time.sleep(1.5)
            articles = self.driver.find_elements(By.CSS_SELECTOR, "article a")
            links_dict = {"page" : i+1, "links" : []}
            for article in articles:
                try:
                    href = article.get_attribute("href")
                    if href and (href not in links_dict["links"]):
                        links_dict['links'].append(href)
                except:
                    continue
            self.article_links.append(links_dict)
            print(f"{i+1}페이지 링크 리스트({len(links_dict['links'])}개) : \n{links_dict}")

    # 기사제목과 원본 추출
    def extract_article_data(self, url, index, page):
        self.driver.get(url)
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "section.article-wrap h1").text
        except:
            title = "제목없음"
        
        try:
            # 기사 본문 p 태그 리스트 추출
            paragraphs = self.driver.find_elements(By.CSS_SELECTOR, "p.content_text.text-l")
            # 텍스트만 추출 후 \n으로 연결
            content = "\n".join([p.text.strip() for p in paragraphs])
            if content == "" or bool(re.fullmatch(r'\n*', content)): return None
        except:
            return None

        print(f"✅ 수집 완료: {title[:20]}... / {content[:20]}...")
        return DataArticle(**{
            "title": title, 
            "content": content, 
            "url" : url, 
            "index" : index+1, 
            "page" : page, 
            "keyword" : self.keyword,
            "site" : self.site,
            "media" : self.site
        })
    
if __name__ == "__main__":
    crawler = KhanCrawler(keyword="이재명", site="khan")
    crawler.run()