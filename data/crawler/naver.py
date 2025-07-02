from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# ✅ 크롬 옵션 설정
options = Options()
# options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 10)

# ✅ 메인 페이지 진입 및 기사 링크 수집
driver.get("https://n.news.naver.com/section/100")

# '더보기' 버튼 클릭 3번
for _ in range(10):
    try:
        more_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.section_more_inner._CONTENT_LIST_LOAD_MORE_BUTTON")))
        driver.execute_script("arguments[0].click();", more_btn)
        time.sleep(1.5)
    except Exception as e:
        print("더보기 클릭 실패:", e)
        break

# 기사 링크 수집
article_links = list({
    elem.get_attribute("href")
    for elem in driver.find_elements(By.CSS_SELECTOR, "a.sa_text_title._NLOG_IMPRESSION")
    if elem.get_attribute("href")
})

print(f"총 기사 수집 링크 수: {len(article_links)}")

# ✅ 각 기사 페이지 접근 후 정보 수집
results = []
for url in article_links:
    try:
        driver.get(url)
        wait.until(EC.presence_of_element_located((By.ID, "dic_area")))

        title = driver.find_element(By.CSS_SELECTOR, "h2.media_end_head_headline").text.strip()
        body = driver.find_element(By.ID, "dic_area").text.strip()

        # 날짜 정보
        date_span = driver.find_element(By.CSS_SELECTOR, "span.media_end_head_info_datestamp_time._ARTICLE_DATE_TIME")
        pub_date = date_span.text.strip()

        # 신문사 이름
        try:
            # 방식 1: img 태그의 alt 속성으로 가져오기 (가장 정확함)
            press_logo = driver.find_element(By.CSS_SELECTOR, "a.media_end_linked_title_inner img")
            press_name = press_logo.get_attribute("alt").strip()
        except:
            try:
                # 방식 2: span 태그의 textContent 가져오기 (fallback)
                press_name = driver.find_element(
                    By.CSS_SELECTOR, "span.media_end_linked_title_text.dark_type._LAZY_LOADING_ERROR_SHOW"
                ).text.strip()
            except:
                press_name = ""        
        print(f"신문사: {press_name}, 제목: {title}, 날짜: {pub_date}")
        results.append({
            "신문사": press_name,
            "기사제목": title,
            "본문": body,
            "작성일자": pub_date,
            "URL": url
        })

        time.sleep(0.5)
    except Exception as e:
        print(f"크롤링 실패 ({url}): {e}")
        continue

# ✅ DataFrame → 엑셀 저장
df = pd.DataFrame(results)
df.to_excel("result.xlsx", index=False)
df.to_json("result.json", orient="records", force_ascii=False)
print("✅ 엑셀 파일(result.xlsx) 저장 완료")

driver.quit()
