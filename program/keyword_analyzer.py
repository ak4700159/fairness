# langchain 패키지
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain.evaluation.criteria import CriteriaEvalChain

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import program.fair_setup as fair_setup 
from operator import itemgetter

"""
역할 : 사용자 검색 프롬프트를 바탕으로 예시와 같이 다방면으로 해석 가능한지 판별, 만약 가능하다면 카테고리 부여 
기능 :
    1. 검색 프롬프트를 바탕으로 다방면으로 해석 가능한 프롬프트인지 판별
    2. 다방면으로 해석 가능한 경우 카테고리 추출 및 부여
    3. 해당 답변을 평가하기
"""
class KeywordAnalyzer:
    def __init__(self):
        self.llm = fair_setup.load_gpt_model(r"config.yaml")
        self.criteria = {
            "relevance" : "만약 응답이 입력에 대해 카테고리 별로 분류한 응답인 경우, 추출된 카테고리가 사용자 프롬프트와 관련성이 있는가?",
            "diversity" : "만약 응답이 입력에 대해 카테고리 별로 분류한 응답인 경우, 카테고리 간 관점이 실제로 상충되는 입장인가?",
            "nothing" : "입력에 대해 카테고리 별로 분류하지 않았다면(응답 : no/아니요) 이에 대해 충분히 논리적으로 설명하고 있는가?"
        }

    # 전체 체인 구성 
    def run(self, user_prompt):
        judge_chain = self.getJudgeChain()
        main_chain = (
            {"response" : judge_chain, "user_prompt" : itemgetter("user_prompt")}
            | RunnableLambda(self.route)
            | StrOutputParser()
        )
        return main_chain.invoke({"user_prompt" : user_prompt})
    
    # 비동기 실행
    async def asyncRun(self, user_prompt):
        judge_chain = self.getJudgeChain()
        main_chain = (
            {"response" : judge_chain, "user_prompt" : itemgetter("user_prompt")}
            | RunnableLambda(self.route)
            | StrOutputParser()
        )
        return await main_chain.ainvoke({"user_prompt" : user_prompt})

    """
        카테고리를 생성하는 체인 생성
    """
    def getCategoryChain(self):
        chat_prompt = ChatPromptTemplate.from_template(
            """
                주어진 사용자 프롬프트로부터 다방면으로 해석될 수 있는 카테고리를 추출해주세요. 서로 다른 해석, 입장, 논리가 제시할 수 있는 카테고리여야 합니다.
                예를 들어 종교(종교별 해석), 정치(진보 진영, 보수 진영, 중도), 국가(민족별, 지역별 해석), 세대(10대, 20대, 30대, 기성세대, MZ세대 등), 성별(남녀) 등 대표적인 집단적 특성을 가지고 대립되는 의견이 나올 수 있는 카테고리를 추출하면 됩니다.
                답변 예시 : "정치" : ["진보측면", "보수측면"], "인종" : ["황인", "백인"], "이유" : "해당 키워드는 ~~ 이유 때문에 정치, 인종 카테고리로 해석할 수 있습니다."
                사용자 프롬프트(질문) : {user_prompt}
                답변 : 
            """
        )

        # 체인 반환
        return (
            chat_prompt
            | self.llm
        )
    
    def getReasonChain(self):
        chat_prompt = ChatPromptTemplate.from_template(
            """
                다음과 같은 질문을 했을 때 왜 아니요 라는 답변이 나왔는지 설명하시오
                주어진 사용자 프롬프트가 서로 다른 해석, 입장, 논리가 제시할 수 있는지 판별주세요. 답변은 언제나 한 단어로 예 또는 아니요로 답변해주세요.
                예를 들어 종교(종교별 해석), 정치(진보 진영, 보수 진영, 중도), 국가(민족별, 지역별 해석), 세대(세대별 해석), 성별(남녀) 등 대표적인 집단적 특성을 가지고 대립되는 의견이 나올 수 있는지를 중점으로 판별하면 됩니다.
                사용자 프롬프트 : {user_prompt} 
            """
        )
        return (chat_prompt | self.llm)

    """
        다방면으로 검색되는지 판단하는 체인 생성
    """
    def getJudgeChain(self):
        chat_prompt = ChatPromptTemplate.from_template(
            """
                주어진 사용자 프롬프트가 서로 다른 해석, 입장, 논리가 제시할 수 있는지 판별주세요. 답변은 언제나 한 단어로 yes 또는 no로 답변해주세요.
                예를 들어 종교(종교별 해석), 정치(진보 진영, 보수 진영, 중도), 국가(민족별, 지역별 해석), 세대(세대별 해석), 성별(남녀) 등 대표적인 집단적 특성을 가지고 대립되는 의견이 나올 수 있는지를 중점으로 판별하면 됩니다.
                (답변 예시)
                질문1 : 윤석열 
                답변1 : yes
                ==================================
                질문2 : 기하학이란?
                답변2 : no
                ==================================
                사용자 프롬프트(질문) : {user_prompt}
                답변 :  
            """
        )
        # 체인 반환
        return (
            chat_prompt
            | self.llm
        )
    
    """
        응답 분석 후 라우팅 함수
    """
    def route(self, info):
        judge_result = info.get("response").content.strip().lower()
        if judge_result == "yes":
            return self.getCategoryChain()
        elif judge_result == "no":
            return self.getReasonChain()
        # 제대로 응답하지 못한 경우
        return (
            ChatPromptTemplate.from_template(
                """
                    해당 키워드를 다방면으로 카테고리를 분류할 수 있는지 판단을 위해 네/아니요 대답을 못해 라우팅하지 못하였음을 알린다.(시스템 오류)
                    사용자 프롬프트 : {user_prompt} 
                """
            ) 
            | self.llm
        )

    """
        응답 결과 평가하기(LLM 모델을 통해 추론)
    """
    async def asyncEvaluate(self, prediction, input, index):
        evaluator = CriteriaEvalChain.from_llm(llm=self.llm, criteria=self.criteria)
        result = await evaluator.aevaluate_strings(prediction=prediction, input=input)
        print(f"{index}번째 키워드 평가 결과 : score={result['score']} / value={result['value']}")
        return {
            "index" : index,
            "score" : result['score'],
            "value" : result['value'],
            "user_pomrpt" : input,
            "prediction" : prediction,
        }