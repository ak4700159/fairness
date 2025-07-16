from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import time
import json
import re

# https://www.koreadaily.com/search?searchWord=%EB%AF%BC%EC%83%9D+%EC%A0%95%EC%B1%85&searchType=all&highLight=true&page=1
class KoreaCrawler:
    def __init__(self, keyword, max_pages=5):
        self.keyword = keyword
        self.max_pages = max_pages
        self.driver = None
        self.wait = None
        self.article_links = []
        self.results = [] # [{"기사제목" : "기사제목", "기사본문" : "기사본문"}, {"기사제목" : "기사제목", "기사본문" : "기사본문"},]

    # 패키지 드라이버 세팅 
    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')  # UI 숨기기 옵션 제거 
        options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        self.wait = WebDriverWait(self.driver, 10)
        print("✅ WebDriver 초기화 완료")
    
    # 기사링크 수집
    def collect_article_links(self):
        for i in range(self.max_pages):
            base_url = f"https://www.koreadaily.com/search?searchWord={self.keyword}&searchType=all&highLight=true&page={i+1}"
            self.driver.get(base_url)
            time.sleep(1.5)
            articles = self.driver.find_elements(By.CSS_SELECTOR, "div.newsList a")
            links = set()
            for article in articles:
                try:
                    href = article.get_attribute("href")
                    if href:
                        links.add(href)
                except:
                    continue
            self.article_links.extend(links)
            print(f"{i+1}페이지 링크 리스트({len(links)}개) : \n{links}")

    # 기사제목과 원본 추출
    def extract_article_data(self, url):
        self.driver.get(url)
        try:
            title = self.driver.find_element(By.CSS_SELECTOR, "div.headline h1").text
        except:
            title = ""
        
        try:
            # 기사 본문 p 태그 리스트 추출
            content = self.driver.find_element(By.CSS_SELECTOR, "section#newsBody").text
            # 텍스트만 추출 후 \n으로 연결
            # content = "\n".join([p.text.strip() for p in paragraphs])
            if content == "" or bool(re.fullmatch(r'\n*', content)): return None
        except:
            return None

        print(f"✅ 수집 완료: {title[:20]}... / {content[:20]}...")
        return {"기사제목": title, "기사본문": content, "신문사" : "중앙일보", "URL" : url}

    # 기사 수집 함수
    def collect_articles(self):
        for url in self.article_links:
            article = self.extract_article_data(url)
            if article != None:
                self.results.append(article)


    # 수집된 기사 저장 함수
    def save_to_file(self, save_path=".", file_name="korea_articls.json"):
        if self.results == []:
            print("수집된 기사 없습니다.")
            return
        full_path = f"{save_path}/{file_name}"
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"✅ 파일 저장 완료: {full_path}")
        

    def run(self):
        self.setup_driver()
        self.collect_article_links()
        self.collect_articles()
        self.save_to_file()
        print("🧹 드라이버 종료 및 작업 완료")

if __name__ == "__main__":
    crawler = KoreaCrawler(keyword="민생 지원",max_pages=3)
    crawler.run()
