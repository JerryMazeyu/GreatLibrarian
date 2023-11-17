from Agents import BookStore, PromptMarket
from LLMs import *
from Interactor import *
from FinalScore import *


class ExampleConfig():
    def __init__(self):
        # self.llm = chatglm_pro
        # self.llm = qwen_turbo
        self.llm = wenxin
        self.json_paths = ['example1.json','example2.json','example3.json','example4.json','example5.json','example6.json','example7.json']
        self.interactor = AutoInteractor
        self.finalscore = FinalScore1
        # self.register_agents = [BookStore]


class ExampleConfig():
    def __init__(self):
        # self.llm = chatglm_pro
        self.llm = qwen_turbo
        # self.llm = wenxin
        self.json_paths = ['example11.json','example12.json','example13.json','example14.json','example15.json','example16.json','example17.json','example18.json','example19.json','example20.json']
        self.interactor = AutoInteractor
        self.finalscore = FinalScore1
        # self.register_agents = [BookStore, PromptMarket]

# class ExampleConfig():
#     def __init__(self):
#         self.llm = chatglm6b
#         self.json_paths = ['example1.json']
#         # self.register_agents = [BookStore, PromptMarket]
#         # self.interactor = AutoInteractor
        
exconf = ExampleConfig()