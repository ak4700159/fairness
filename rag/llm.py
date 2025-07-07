from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class GPT:
    def __init__(self, model="gpt-4.1"):
        self.llm = ChatOpenAI(model=model)
        # self.output_parser = JsonOutputParser(pydantic_object=ArticleJson)
        # self.format_instructions = self.output_parser.get_format_instructions()

        # self.prompt_template = PromptTemplate(
        #     template="주어진 기사 본문 : {content} "
        #              "\n 기사제목 : {title}를 보고 새로운 기사 본문과 제목를 생성해주세요. "
        #              "주어진 기사의 내용을 바탕으로 작성해야되며 주어진 기사와 비슷한 어조를 사용하고 "
        #              "인터뷰 내용이 있다면 반대되는 의견으로 비슷하게 작성해야됩니다. "
        #              "생성된 본문을 자극적으로 나타내는 기사제목을 작성해야 되고 분량은 원본 분량과 비슷해야합니다."
        #              "\n {format_instructions}",
        #     input_variables=["title", "content"],
        #     partial_variables={"format_instructions": self.format_instructions},
        # )
        # self.chain = self.prompt_template | self.llm | self.output_parser