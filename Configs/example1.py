from Agents import BookStore, PromptMarket
from LLMs import chatglm6b
from Interactor import *


class ExampleConfig():
    def __init__(self):
        self.llm = chatglm6b
        self.json_paths = ['example1.json', 'example2.json']
        self.register_agents = [BookStore, PromptMarket]
        self.interactor = AutoInteractor

class ExampleConfig():
    def __init__(self):
        self.llm = chatglm6b
        self.json_paths = ['example1.json']
        # self.register_agents = [BookStore, PromptMarket]
        # self.interactor = AutoInteractor
        
exconf = ExampleConfig()