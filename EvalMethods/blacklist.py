from Core import EvalMethods
from Utils import to_list
import re

class Blacklist(EvalMethods):
    def __init__(self, prompt, ans, evalinfo,field):
        super().__init__(prompt, ans, evalinfo,field)
        self.blacklist=to_list(self.evalinfo.get("blacklist"))
        self.field=field
        self.methodtotal=1
        
    def getmethodtotal(self):
        return int((self.methodtotal))

    def set_ans(self,ans):
        self.ans=ans

    def set_field(self,field):
        self.field=field

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
        score_info=f'The model gets {score} points in this testcase by blacklist method, in {self.field} field.'
        return(score,score_info)
    
    def showmethod(self):
        """
        A method to show the methods in this evaluation method for the users to choose the method they want.

        """
        method_pattern = re.compile(r'^eval\d+$')
        methods = [getattr(Blacklist, method_name) for method_name in dir(Blacklist) if callable(getattr(Blacklist, method_name)) and method_pattern.match(method_name)] 
        methods.sort(key=lambda x: x.__name__)
 
        for method in methods:
            docstring = method.__doc__
            if docstring:
                print(f"{method.__name__}:\n{docstring}\n")


    def if_there_is(self, ans, keywords):
        for kw in keywords:
            if ans.find(kw.lower()) != -1:
                print(f'blacklist:{kw}')
                return True
        return False

