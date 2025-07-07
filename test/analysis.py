from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# # prompt + model + output parser
# prompt = ChatPromptTemplate.from_template("You are an expert in astronomy. Answer the question. <Question>: {input}")
# llm = ChatOpenAI(model="gpt-4o-mini")
# output_parser = StrOutputParser()

# # LCEL chaining
# chain = prompt | llm | output_parser

# # chain 호출
# print(chain.invoke({"input": "지구의 자전 주기는?"}))


prompt1 = ChatPromptTemplate.from_template("translates {korean_word} to English.")
prompt2 = ChatPromptTemplate.from_template(
    "explain {english_word} using oxford dictionary to me in Korean."
)
llm = ChatOpenAI(model="gpt-4o-mini")
chain1 = prompt1 | llm | StrOutputParser()
chain2 = (
    {"english_word": chain1}
    | prompt2
    | llm
    | StrOutputParser()
)
print(chain2.invoke({"korean_word":"미래"}))