from selenium.webdriver.common.by import By
import time
import re
from crawler.crawler import Crawler 
from article import Article as DataArticle

# https://www.chosun.com/nsearch/?query={}&page={}&siteid=&sort=1&date_period=&date_start=&date_end=&writer=&field=&emd_word=&expt_word=&opt_chk=false&app_check=0&website=www,chosun&category=
class ChosunCrawler(Crawler):
    # 기사링크 수집
    def collect_article_links(self):
        for i in range(self.max_pages):
            base_url = f"https://www.chosun.com/nsearch/?query={self.keyword}&page={i+1}&siteid=&sort=1&date_period=&date_start=&date_end=&writer=&field=&emd_word=&expt_word=&opt_chk=false&app_check=0&website=www,chosun&category="
            self.driver.get(base_url)
            time.sleep(1.5)
            articles = self.driver.find_elements(By.CSS_SELECTOR, "div.story-card-right a.text__link.story-card__headline")
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

    # 기사제목과 기사본문 추출
    def extract_article_data(self, url, index, page):
        self.driver.get(url)
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "h1.article-header__headline").text
        except:
            title = ""
        
        try:
            # 기사 본문 p 태그 리스트 추출
            contents = self.driver.find_elements(By.CSS_SELECTOR, "p.article-body__content.article-body__content-text")
            # 텍스트만 추출 후 \n으로 연결
            content = "\n".join([p.text.strip() for p in contents])
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
    crawler = ChosunCrawler(keyword="이재명", site="chosun")
    crawler.run()