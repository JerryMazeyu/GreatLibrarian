from ...Core import Agents
import os


class BookStore(Agents):

    def __init__(self):
        self.data_root = "Agents/BookStore/RawData"
        self.subjects = os.listdir(self.data_root)

    def __call__(self, prompt: str) -> str:
        pass

    def process(self, sql):
        pass

    def help(self):
        pass
