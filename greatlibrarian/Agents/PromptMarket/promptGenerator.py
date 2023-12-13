#!pip install langchain
#!pip install openai
""""""

from langchain.llms import OpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import os

os.environ["OPENAI_API_KEY"] = "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"
"""environment configuration"""

"""This is intended to generate formatted prompts for the LLM to get the response from LLM
   args: domain, num,
   input: domain name you want to ask
   return: answer
"""
llm = OpenAI(temperature=0.0)


# 创建与角色相关联的消息模板使用MessagePromptTemplate
"""方法1"""
"""简单的prompt模板生成"""
# prompt=PromptTemplate(
#     input_variables=["domain"],
#     template="tell me three points about {domain}."
# )

# print(prompt.format(domain="math"))
openai_api_key = os.environ["OPENAI_API_KEY"]
mytext = "介绍下ChatGPT"
print(llm(mytext))

"""方法2"""
"""生成模板+与llm交互-单轮对话"""
# print("请输入您的领域，按Enter结束")
# var=input()
# template = "你是{value}方面的专家，你需要给我三条该领域内的知识点，包括原理、特点和使用范围。"
# prompt = PromptTemplate(
#     input_variables=["value"],
#     template=template,
#     )
# final_prompt = prompt.format(value=var)
# print("输入内容：:", final_prompt)
# print("LLM输出:", llm(final_prompt))

"""生成模板+与llm交互-多轮对话"""
