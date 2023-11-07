from Agents import BookStore, PromptMarket
from LLMs import chatglm_pro
from Interactor import *
from FinalScore import *


class ExampleConfig():
    def __init__(self):
        self.llm = chatglm_pro
        self.json_paths = ['example.json']
        self.interactor = AutoInteractor
        self.finalscore = FinalScore1
        # self.register_agents = [BookStore]


# class ExampleConfig():
#     def __init__(self):
#         self.llm = chatglm6b
#         self.json_paths = ['example5.json']
#         self.register_agents = [BookStore, PromptMarket]
#         self.interactor = AutoInteractor

# class ExampleConfig():
#     def __init__(self):
#         self.llm = chatglm6b
#         self.json_paths = ['example1.json']
#         # self.register_agents = [BookStore, PromptMarket]
#         # self.interactor = AutoInteractor
        
exconf = ExampleConfig()