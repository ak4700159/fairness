from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class ArticleGenerator:
    def __init__(self, template):
        # LLM 모델 설정, 이번 년도 4월에 출시한 gpt-4.1 모델을 사용
        self.llm = ChatOpenAI(model="gpt-4.1")
        # JSON 형태로 출력하기 위한 파서 설정
        output_parser = JsonOutputParser(pydantic_object=ArticleJson)
        # 파서의 포맷 지침 가져오기
        format_instructions = output_parser.get_format_instructions()
        # 프롬프트 템플릿 설정
        self.prompt_template = PromptTemplate(
            template=template,
            input_variables=["title", "content"],
            partial_variables={"format_instructions": format_instructions},
        )
        self.chain = self.prompt_template | self.llm | output_parser

    # 비동기식 
    async def generate(self, title, body):
        # 한번만 복구 시도 
        try:
            response = await self.chain.ainvoke({"title": title, "content": body})
        except Exception as e:
            try:
                print("재시도...")
                response = await self.chain.ainvoke({"title": title, "content": body})
            except Exception as e:
                print(f"재시도 중 오류 발생: {e}")
                response = None
        return response
    
class ArticleJson(BaseModel):
    title: str = Field(..., description="기사 제목")
    content: str = Field(..., description="기사 본문")
