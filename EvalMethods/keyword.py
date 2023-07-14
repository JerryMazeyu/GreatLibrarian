from Core import EvalMethods
from Utils import to_list

class Keyword(EvalMethods):
    def __init__(self, prompt, ans, evalinfo):
        super().__init__(prompt, ans, evalinfo)
        
    
    def eval1(self):
        score = 0.0
        keywords = self.evalinfo['keyword']
        keywords = to_list(keywords)
        for ind, pt in enumerate(self.prompt):
            if self.if_there_is(self.ans[ind], self.keywords):
                score += 1 / len(self.prompt)
        return score
    
    def if_there_is(self, ans, keywords):
        for kw in keywords:
            if ans.find(kw) != -1:
                return True
        return False

