from greatlibrarian.Core import LLMs
import dashscope
from greatlibrarian.Interactor import *
from greatlibrarian.FinalScore import *
# import unittest
# from unittest.mock import patch
# from unittest.mock import MagicMock

class test_llm(LLMs):
    def __init__(self):
        self.apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8"
        self.name = "qwen_turbo"
    
    def __call__(self, prompt: str) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt
        )

        if response:
            if response['output']:
                if response['output']['text']:
                    return(response['output']['text'])
        return('API Problem')


class Config():
    def __init__(self,llm,interactor,finalscore):
        self.llm = llm
        self.interactor = interactor
        self.finalscore = finalscore

config = Config(test_llm,AutoInteractor,FinalScore1)