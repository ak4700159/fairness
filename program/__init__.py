import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import setup 
import program.keyword_analyzer as ka
import asyncio


"""
비동기 분석 실행 함수
parms:
    index : 테스트 데이터 더미 속 인덱스
    analyzer : 키워드 분석기
    user_pomrt : 사용자 프롬프트(키워드)
return:
    type : dict
    response : Agent 응답 결과
    user_prompt : 사용자 프롬프트(키워드),
    index : 테스트 데이터 더미 속 인덱스
"""
async def analyze(index, analyzer, user_prompt):
    result = await analyzer.asyncRun(user_prompt=user_prompt)
    # print(f"{index + 1} 번째 키워드 : {user_prompt}")
    # print(f"결과 답변 : {result}")
    return {"response" : result, "index" : index, "user_prompt" : user_prompt}

async def main():
    # 비동기 작업 모음
    tasks = []
    # 테스트 키워드 더미 
    keywords = [
        "윤석열",
        "길고양이",
        "길고양이 밥주기",
        "윤석열 체포 긍정",
        "윤석열 체포 부정",
        # "RAG",
        # "625 전쟁",
        # "화학 원소란?",
        # "대한민국 출산률 하락의 원인",
        # "하느님과 하나님의 차이",
        # "청년 세대 노동시장 변화",
        # "4 + 2 = ?",
        # "영화 너의 이름은",
        # "이태원참사",
        # "pip install 오류 해결",
        # "가짜뉴스와 사회 혼란",
        # "청년 실업률 통계",
        # "인공지능 모델 편향 사례",
    ]

    # 분석 인스턴스 생성
    analyzer = ka.KeywordAnalyzer()
    # 분석 실행
    for idx, keyword in enumerate(keywords):
        tasks.append(analyze(idx, analyzer, keyword))
    results = await asyncio.gather(*tasks)
    tasks.clear()
    # 분석에 대한 평가 실행
    for result in results:
        tasks.append(analyzer.asyncEvaluate(result['response'], result['user_prompt'], result['index']))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # 환경변수 설정 
    setup.set_config(r"config.yaml", "[0717 fair search app] evaluate llm")
    # main coroutine 실행 
    asyncio.run(main())