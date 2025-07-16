from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_teddynote import logging
from pydantic import BaseModel, Field
import sys
from setup import set_config
import json

class ResponseJson(BaseModel):
    score: float = Field(..., description=" 기사글에 대해 부정적인 긍정적인, 중립적인지(알 수 없는, 모호한)를 판단하기 위해 -1(부정) ~ 0(중립) ~ 1(긍정)으로 수치(실수, 소수점 둘째자리까지만 고려)")
    reason: str = Field(..., description="score가 이렇게 나온 이유에 대한 설명")

def log_article_result(idx, title, score, reason):
    print(f"[{idx}] ✅ 제목: {title[:30]}...")
    print(f"     ➤ 점수: {score:.2f}")
    print(f"     ➤ 이유: {reason[:80]}...")

# 4. 이를 GPT에게 전달해 키워드에 대해 해당 기사글이 부정적인지, 긍정적인지, 알 수 없는지(모호, 중립)를 판단.
# 5. -1(부정) ~ 0(중립) ~ 1(긍정)으로 수치로 할당
if __name__ == "__main__":
    set_config(project_name="07/17 article analyze")
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
                                             
        수치 : -0.95
        이유 : 감옥, 내란죄와 같이 윤석열에 대해 부정적인 시각이 드러났기 때문입니다.
        
        사용자 키워드 : {user_prompt}
        기사 제목 : {title}
        기사 본문 : {content}        
        출력 형식 : {format_instructions}
    """)
    chain = prompt | llm | output_parser

    # 전체 기사 불러오기
    with open(r"data\dumy\total_articls.json", 'r', encoding='utf-8') as f:
        articles = json.load(f)

    results = []
    for idx, article in enumerate(articles):
        response = chain.invoke({"user_prompt" : "민생 지원", "title" : article['기사제목'], "content" : article['기사본문'], "format_instructions" : output_parser.get_format_instructions()})
        results.append({
            "keyword" : "민생 지원",
            "title" : article['기사제목'], 
            "content" : article['기사본문'], 
            "media" : article['신문사'],
            "url" : article['URL'],
            "score" : response['score'], 
            "reason" : response['reason']
        })
        log_article_result(idx + 1, article['기사제목'], response['score'], response['reason'])

    with open(r"data\dumy\result2.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("✅ 모든 기사 처리 완료")


