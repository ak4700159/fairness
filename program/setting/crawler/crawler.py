from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta, timezone
import json
import os

class Crawler(ABC):
    def __init__(self, keyword, site, max_pages=5):
        self.keyword = keyword
        self.search_datetime = ""
        self.max_pages = max_pages
        self.site = site
        self.driver = None
        self.wait = None
        self.article_links = [ ]
        self.results = []

    # 패키지 드라이버 세팅 
    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')  # UI 숨기기 옵션 제거 
        options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=options)
        self.wait = WebDriverWait(self.driver, 10)

        # 현재 시각을 검색 시간으로 설정
        KST = timezone(timedelta(hours=9))
        kst_now = datetime.now(KST)
        self.search_datetime = kst_now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"✅{self.site} WebDriver 초기화 완료 {self.search_datetime}")

    @abstractmethod
    def collect_article_links(self):
        pass

    @abstractmethod
    def extract_article_data(self, url, index, page):
        pass

    # 기사 수집 함수
    def collect_articles(self):
        for link_dict in self.article_links:
            for idx, url in enumerate(link_dict['links']):
                article = self.extract_article_data(url=url, index=idx, page=link_dict['page'])
                if article != None:
                    self.results.append(article)

    # 수집한 데이터 저장하기
    def save_to_file(self, save_path=None, file_name="result.json"):
        if self.results == []:
            print("수집된 기사 없습니다.")
            return
        json_data = [article.to_dict() for article in self.results]
        # 🟢 저장 경로를 실행 파일 위치 기준으로 고정: FAIRNESS/data/dumy/
        if save_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치: e.g. FAIRNESS/data/crawler/
            base_dir = os.path.abspath(os.path.join(current_dir, ".."))  # 한 단계 위로: FAIRNESS/data/
            save_path = os.path.join(base_dir, "dumy")  # -> FAIRNESS/data/dumy/
        # 디렉토리가 없으면 생성
        os.makedirs(save_path, exist_ok=True)
        full_path = os.path.join(save_path, f"{self.site}_{file_name}")

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✅ {len(json_data)}개 기사 파일 저장 완료: {full_path}")

    # def save_to_database(self):
    #     # 데이터베이스 호출 후 results 결과 파일 저장
    #     pass

    # 크롤링 실행  
    def run(self):

        # 드라이버 초기 세팅
        self.setup_driver()
        # 기사 링크 수집
        self.collect_article_links()
        # 기사 수집
        self.collect_articles()
        print("🧹 드라이버 종료 및 작업 완료")


