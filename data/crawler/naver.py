from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

class NaverNewsCrawler:
    def __init__(self, base_url="https://n.news.naver.com/section/100", max_clicks=10):
        self.base_url = base_url
        self.max_clicks = max_clicks
        self.driver = None
        self.wait = None
        self.article_links = []
        self.results = []

    def setup_driver(self):
        options = Options()
        # options.add_argument('--headless')  # UI 숨기기 옵션 제거 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.wait = WebDriverWait(self.driver, 10)
        print("✅ WebDriver 초기화 완료")

    def collect_article_links(self):
        print("📍 기사 링크 수집 시작")
        self.driver.get(self.base_url)

        for i in range(self.max_clicks):
            try:
                more_btn = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "a.section_more_inner._CONTENT_LIST_LOAD_MORE_BUTTON")
                ))
                self.driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(1.5)
            except Exception as e:
                print(f"⚠️ 더보기 클릭 실패 (클릭 {i+1}회):", e)
                break

        links = {
            elem.get_attribute("href")
            for elem in self.driver.find_elements(By.CSS_SELECTOR, "a.sa_text_title._NLOG_IMPRESSION")
            if elem.get_attribute("href")
        }

        self.article_links = list(links)
        print(f"✅ 수집된 기사 링크 수: {len(self.article_links)}")

    def extract_article_data(self, url):
        try:
            self.driver.get(url)
            self.wait.until(EC.presence_of_element_located((By.ID, "dic_area")))

            title = self.driver.find_element(By.CSS_SELECTOR, "h2.media_end_head_headline").text.strip()
            body = self.driver.find_element(By.ID, "dic_area").text.strip()

            date_span = self.driver.find_element(By.CSS_SELECTOR, "span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME")
            pub_date = date_span.text.strip()

            try:
                press_logo = self.driver.find_element(By.CSS_SELECTOR, "a.media_end_linked_title_inner img")
                press_name = press_logo.get_attribute("alt").strip()
            except:
                try:
                    press_name = self.driver.find_element(
                        By.CSS_SELECTOR, "span.media_end_linked_title_text.dark_type._LAZY_LOADING_ERROR_SHOW"
                    ).text.strip()
                except:
                    press_name = ""

            print(f"📰 {press_name} | {title} | {pub_date}")

            return {
                "신문사": press_name,
                "기사제목": title,
                "본문": body,
                "작성일자": pub_date,
                "URL": url
            }

        except Exception as e:
            print(f"❌ 크롤링 실패 ({url}): {e}")
            return None

    def collect_articles(self):
        print("📍 기사 내용 수집 시작")
        for url in self.article_links:
            data = self.extract_article_data(url)
            if data:
                self.results.append(data)
            time.sleep(0.5)

    def save_to_file(self, excel_path="result.xlsx", json_path="result.json"):
        df = pd.DataFrame(self.results)
        df.to_excel(excel_path, index=False)
        df.to_json(json_path, orient="records", force_ascii=False)
        print(f"✅ 저장 완료: {excel_path}, {json_path}")

    def run(self):
        self.setup_driver()
        self.collect_article_links()
        self.collect_articles()
        self.save_to_file()
        self.driver.quit()
        print("🧹 드라이버 종료 및 작업 완료")