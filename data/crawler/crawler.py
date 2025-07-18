from abc import ABC, abstractmethod
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import json

class Crawler(ABC):
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

    @abstractmethod
    def collect_article_links(self):
        pass

    @abstractmethod
    def extract_article_data(self):
        pass

    @abstractmethod
    def collect_articles(self):
        pass

    # 수집한 데이터 저장하기
    def save_to_file(self, save_path=".", file_name="result.json"):
        if self.results == []:
            print("수집된 기사 없습니다.")
            return
        full_path = f"{save_path}/{file_name}"
        with open(full_path, "a", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"✅ 파일 저장 완료: {full_path}")

    def save_to_database(self):
        pass

    # 크롤링 실행  
    def run(self):
        self.setup_driver()
        self.collect_article_links()
        self.collect_articles()
        self.save_to_file()
        print("🧹 드라이버 종료 및 작업 완료")


