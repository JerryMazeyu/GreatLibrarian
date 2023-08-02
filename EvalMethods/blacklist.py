from Core import EvalMethods
from Utils import to_list

class Blacklist(EvalMethods):
    def __init__(self, prompt, ans, evalinfo):
        super().__init__(prompt, ans, evalinfo)
        self.blacklist=to_list(self.evalinfo.get("blacklist"))
        self.methodnum=1
        
    def set_ans(self,ans):
        self.ans=ans

    def eval1(self):
        """
        A method for scoring models based on blacklist.
        Rule:For each propmt,if the model's response that contains at least one of the words in the blacklist, it will get a score of 0 in this evaluation method.
        Returns:Score of the model.

        """
        score = 1.0
        blacklist = self.evalinfo['blacklist']
        blacklist = to_list(blacklist)
        for ind, pt in enumerate(self.prompt):
            if self.if_there_is(self.ans[ind], self.blacklist[ind]):
                score=0
                return score
        return score

    def score(self,method_num):
        """
        A method for choosing one of the methods in keywords to score the model.
        Given a number n and the method will choose the nth eval_method to score the model and print the score. (the number n starts from 1)
        The function will return a string like 'The model gets ***{score}*** points in this testcase by keywords method.'

        """
        eval_dict={1:self.eval1}
        eval_method=eval_dict[method_num]
        score=eval_method()
        score_info=f'The model gets {score} points in this testcase by keywords method.'
        return(score_info)


    def if_there_is(self, ans, keywords):
        for kw in keywords:
            if ans.find(kw) != -1:
                return True
        return False

