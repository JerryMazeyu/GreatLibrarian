from ..Agents import BookStore, PromptMarket
from ..LLMs import *
from ..Interactor import *
from ..FinalScore import *

class ExampleConfig():
    def __init__(self,llm,interactor=AutoInteractor,finalscore=FinalScore1):
        self.llm = llm
        self.interactor = interactor
        self.finalscore = finalscore

# class ExampleConfig():
#     def __init__(self):
#         self.llm = qwen_turbo
#         self.json_paths = ['example11.json']
#         self.interactor = AutoInteractor
#         self.finalscore = FinalScore1
#         # self.register_agents = [BookStore, PromptMarket]
        