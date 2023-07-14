from Core import EvalMethods
from Utils import to_list
import warnings

class ToolUse(EvalMethods):
    def __init__(self, prompt, ans, evalinfo):
        super().__init__(prompt, ans, evalinfo)
        if not self.evalinfo.get("tool", None):
            warnings.warn("There is no tool usage.", RuntimeWarning)
        self.tools = to_list(self.evalinfo.get("tool"))
    
    def eval1(self):
        unit_point = 1. / len(self.prompt)
        res = 0.
        for ind, pt in enumerate(self.prompt):
            target_tool = self.tools[ind]['name']
            target_arg = self.tools[ind]['args']
            if self.ans[ind].find(f'{target_tool}') != -1:
                res += unit_point * (2/3)
            if self.ans[ind].find(f'{target_arg}') != -1:
                res += unit_point * (1/3)
        return res
    