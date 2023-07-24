from Core import EvalMethods
from Utils import to_list
import warnings

class GPT4eval(EvalMethods):
    def __init__(self, prompt, ans, evalinfo):
        super().__init__(prompt, ans, evalinfo)
        if not self.evalinfo.get("GPT4eval", None):
            warnings.warn("There is no GPT4eval.", RuntimeWarning)
        self.methodnum=0
