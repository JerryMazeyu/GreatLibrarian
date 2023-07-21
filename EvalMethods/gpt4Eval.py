from Core import EvalMethods
from Utils import to_list
class GPT4eval(EvalMethods):
    def __init__(self, prompt, ans, evalinfo):
        super().__init__(prompt, ans, evalinfo)
        self.methodnum=0
