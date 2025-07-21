from selenium.webdriver.common.by import By
from crawler.crawler import Crawler 
import time
import re
from article import Article as DataArticle

# https://www.koreadaily.com/search?searchWord=%EB%AF%BC%EC%83%9D+%EC%A0%95%EC%B1%85&searchType=all&highLight=true&page=1
class KoreaCrawler(Crawler):
    # 기사링크 수집
    def collect_article_links(self):
        for i in range(self.max_pages):
            base_url = f"https://www.koreadaily.com/search?searchWord={self.keyword}&searchType=all&highLight=true&page={i+1}"
            self.driver.get(base_url)
            time.sleep(1.5)
            articles = self.driver.find_elements(By.CSS_SELECTOR, "div.newsList a")
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
            title = self.driver.find_element(By.CSS_SELECTOR, "div.headline h1").text
        except:
            title = ""
        try:
            # 기사 본문 p 태그 리스트 추출
            content = self.driver.find_element(By.CSS_SELECTOR, "section#newsBody").text
            # 추출된 본문 안에 내용이 공백 또는 개행 문자로만 이루어져 있는지 확인하는 정규식 표현 
            if content == "" or bool(re.fullmatch(r'[ \n]*', content)): return None
            # 개행 문자가 두 개 이상 노출 시 하나로 축약
            content = re.sub(r'\n{2,}', '\n', content)
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
    crawler = KoreaCrawler(keyword="이재명", site="korea")
    crawler.run()
