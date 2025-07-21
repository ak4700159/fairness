from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from fair_setup import set_env, connect_mysql_database
from datetime import timedelta, timezone
from datetime import datetime as dt
import json
import os
import pandas as pd

from crawler.chosun_crawler import ChosunCrawler
from crawler.khan_crawler import KhanCrawler
from crawler.korea_crawler import KoreaCrawler
from crawler.google_crawler import GoogleCrawler
from crawler.naver_crawler import NaverCrawler
from article import Article

from visualize import visaulize

class ResponseJson(BaseModel):
    score: float = Field(..., description=" 기사글에 대해 부정적인 긍정적인, 중립적인지(알 수 없는, 모호한)를 판단하기 위해 -1(부정) ~ 0(중립) ~ 1(긍정)으로 수치(실수, 소수점 둘째자리까지만 고려)")
    reason: str = Field(..., description="score가 이렇게 나온 이유에 대한 설명")

def log_article_result(idx, title, score, reason):
    print(f"[{idx}] ✅ 제목: {title[:30]}...")
    print(f"     ➤ 점수: {score:.2f}")
    print(f"     ➤ 이유: {reason[:80]}...")

def save_to_database(results):
    try:
        connector = connect_mysql_database(config_path="config.yaml")
        cursor = connector.cursor()

        insert_sql = """
            INSERT INTO result (
                title, content, media, site, datetime, search_datetime,
                `index`, page, score, reason, url, keyword
            ) VALUES (
                %(title)s, %(content)s, %(media)s, %(site)s, %(datetime)s, %(search_datetime)s,
                %(index)s, %(page)s, %(score)s, %(reason)s, %(url)s, %(keyword)s
            )
        """

        for result in results:
            cursor.execute(insert_sql, result)

        connector.commit()
        cursor.close()
        connector.close()
        print("✅ DB 저장 완료")
    except Exception as e:
        print(f"❌ 데이터베이스 오류 : {e}")


def crawl(keyword):
    crawlers  = {
        "korea" : KoreaCrawler(keyword=keyword, site="korea", max_pages=2),
        "khan" : KhanCrawler(keyword=keyword, site="khan"),
        "chosun" : ChosunCrawler(keyword=keyword, site="chosun"),
        "naver" : NaverCrawler(keyword=keyword, site="naver"),
        "google" : GoogleCrawler(keyword=keyword, site="google", max_pages=2)
    }
    total_results = []
    for crawler in crawlers.values():
        crawler.run()
        total_results.extend(crawler.results)
    print(f"총 {len(total_results)}개 기사 수집 완료")
    return total_results

#  GPT에게 전달해 키워드에 대해 크롤링된 기사글이 부정적인지, 긍정적인지, 알 수 없는지(모호, 중립)를 판단.
# 5. -1(부정) ~ 0(중립) ~ 1(긍정)으로 수치로 할당
def analyze(articles, keyword):
    # LLM 환경 세팅
    set_env(project_name="07/17 article analyze")
    llm = ChatOpenAI(model="gpt-4.1")
    output_parser = JsonOutputParser(pydantic_object=ResponseJson)
    prompt = ChatPromptTemplate.from_template("""
        사용자의 프롬프트(주제, 키워드)에 대한 기사글에 대해 부정적인 긍정적인, 중립적인지를 
        판단하기 위해 -1(부정) ~ 0(중립) ~ 1(긍정)으로 수치(실수, 소수점 둘째자리까지만 고려)로 할당하고 그에 대한 이유를 작성하시오.
        좀 더 자세하게 이야기하자면 중립인 경우는 해당 키워드에 대해 정보 위주로 설명하거나 키워드에 대해 특정 감정을 표출하지 않는 경우를 말한다.
        부정은 해당 키워드에 대해 부정적인 시각(표현)으로 바라본 경우고 긍정은 긍정적인 시각(표현)을 가지고 키워드를 보도하는 경우입니다.                                      
        ex)
        사용자 키워드 : 윤석열
        기사 제목 : 감옥가자
        기사 본문 : 윤석열은 내란죄이기에 감옥에 가야한다.
                                             
        수치 : -0.98
        이유 : 감옥, 내란죄와 같이 윤석열에 대해 부정적인 시각이 드러났기 때문입니다.
        
        사용자 키워드 : {user_prompt}
        기사 제목 : {title}
        기사 본문 : {content}        
        출력 형식 : {format_instructions}
    """)
    chain = prompt | llm | output_parser

    results = []
    for idx, article in enumerate(articles):
        try:
            response = chain.invoke({"user_prompt" : keyword, "title" : article.title, "content" : article.content, "format_instructions" : output_parser.get_format_instructions()})
        except Exception as e:
            print(f"LLM 응답 오류 발생 : {e}")
            continue
        results.append({
            **article.to_dict(),
            "score" : response['score'], 
            "reason" : response['reason']
        })
        log_article_result(idx + 1, article.title, response['score'], response['reason'])
    print("✅ 모든 기사 처리 완료")
    return results

def save_to_local(results, save_path):
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    keyword = "이재명"
    # 현재 시간 표현, 폴더명에 들어가게됨
    KST = timezone(timedelta(hours=9))
    kst_now = dt.now(KST)
    datetime = kst_now.strftime("%m%d-%H%M")

    # 절대 경로로 결과 내용 저장
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일 위치: e.g. FAIRNESS/data/crawler/
        os.makedirs(os.path.join(current_dir, "dumy"), exist_ok=True)  # 디렉토리 없으면 생성
        save_path = os.path.join(current_dir, "dumy")  # 더미디렉토리에 매핑
        save_path = os.path.join(save_path, f"[{datetime}]{keyword}_result.json")  
    except:
        print("잘못된 파일 접근")

    # 크롤링을 한꺼번에 진행 후 파일병합
    articles = crawl(keyword=keyword)

    print(f"총 {len(articles)}개 기사 크롤링 완료")
    # 크롤링한 기사 분석 및 평가
    results = analyze(articles=articles, keyword=keyword)

    # 분석한 내용 DB server에 저장 + 로컬에도 저장
    save_to_local(results=results, save_path=save_path)
    save_to_database(results=results)

    # 데이터 시각화 
    # visaulize(file_path=r"C:\Users\cn120\바탕 화면\rag\fairness\data\dumy\[07 21-15 52]이재명_result.json", keyword=keyword)
    visaulize(file_path=save_path, keyword=keyword)
