from Core import EvalMethods

class Keyword(EvalMethods):
    def __init__(self, prompt, llm, evalinfo):
        super().__init__(prompt, llm, evalinfo)
    
    
    def eval1(self):
        score = 0.0
        keywords = self.evalinfo['keyword']
        if isinstance(keywords[0], str):
            self.keywords = [keywords]
        for pt in self.prompt:
            ans = self.llm(pt)
            if self.if_there_is(ans, self.keywords):
                score += 1 / len(self.prompt)
        return score
    
    def if_there_is(self, ans, keywords):
        for kw in keywords:
            if ans.find(kw) != -1:
                return True
        return False

