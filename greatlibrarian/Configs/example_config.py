from ..LLMs import *
from ..Interactor import *
from ..FinalScore import *


class ExampleConfig:
    def __init__(
        self, test_llm, GPT4_eval_llm, finalscore=FinalScore1, interactor=AutoInteractor
    ):
        self.test_llm = test_llm
        self.GPT4_eval_llm = GPT4_eval_llm
        self.interactor = interactor
        self.finalscore = finalscore


# class ExampleConfig():
#     def __init__(self):
#         self.llm = qwen_turbo
#         self.json_paths = ['example11.json']
#         self.interactor = AutoInteractor
#         self.finalscore = FinalScore1
#         # self.register_agents = [BookStore, PromptMarket]
