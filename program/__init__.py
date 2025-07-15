import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import setup 
import program.keyword_analyzer as ka

if __name__ == "__main__":
    setup.set_config(r"C:\Users\ksm\Desktop\fairness\config.json")
    keywords = [
        "윤석열",
        "RAG",
        "625 전쟁",
        "화학 원소란?",
        "대한민국 출산률 하락의 원인",
        "하느님과 하나님의 차이",
        "청년 세대 노동시장 변화",
        "4 + 2 = ?",
        "영화 너의 이름은",
        "이태원참사",
        "pip install 오류 해결",
        "가짜뉴스와 사회 혼란",
        "청년 실업률 통계",
        "인공지능 모델 편향 사례",
    ]

    analyzer = ka.KeywordAnalyzer()
    for idx, keyword in enumerate(keywords):
        print(f"{idx + 1} 번째 키워드 : {keyword}")
        result = analyzer.run(user_prompt=keyword)
        print(f"결과 답변 : {result}")
        analyzer.evaluate(result, keyword)
        print("-------------------------------------\n")