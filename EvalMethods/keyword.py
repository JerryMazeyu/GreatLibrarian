from Core import EvalMethods
from Utils import to_list
import re

class Keyword(EvalMethods):
    def __init__(self, prompt, ans, evalinfo,field):
        super().__init__(prompt, ans, evalinfo,field)
        self.name = ['keyword', 'Keyword', 'Keywords','keywords']
        self.keywords=self.evalinfo['keywords']
        self.field=field
        self.methodtotal=2
        
    def getmethodtotal(self):
        return int((self.methodtotal))
    
    def set_ans(self,ans):
        self.ans=ans

    def set_field(self,field):
        self.field=field

    def eval1(self):
        """
        A method for scoring models based on keywords.
        Rule:For each propmt, the model's response that contains at least one of the keywords gets a score of 1/n, and n is the number of prompts.
        Returns:Score of the model.

        """
        score = 0.0
        keywords = self.evalinfo['keywords']
        keywords = to_list(keywords)
        #print(self.prompt)
        #print(self.keywords)
        for ind, pt in enumerate(self.prompt):
            if self.if_there_is(self.ans[ind], self.keywords[ind]):
                score += 1 / len(self.prompt)
        return score
    
    def eval2(self):
        """
        A method for scoring models based on keywords.
        Rule:For each prompt, the model gets a score of 1/n for each keyword included in the response, and n is the number of key words.
        Returns:Score of the model.

        """
        score=0.0
        keywords = self.evalinfo['keywords']
        keywords = to_list(keywords)
        for ind, pt in enumerate(self.prompt):
          for k in keywords[ind]:
              if self.ans[ind].find(k)!=-1:
                  score += 1 / len(self.keywords[ind])*len(self.promopt)
        return(score)
    

    def score(self,method_num):
        """
        A method for choosing one of the methods in keywords to score the model.
        Given a number n and the method will choose the nth eval_method to score the model and print the score. (the number n starts from 1)
        The function will return a string like 'The model gets ***{score}*** points in this testcase by keywords method.'

        """
        eval_dict={1:self.eval1,2:self.eval2}
        eval_method=eval_dict[method_num]
        score=eval_method()
        score_info=f'The model gets {score} points in this testcase by keywords method, in {self.field} field.'
        return(score,score_info)
    
    def showmethod(self):
        """
        A method to show the methods in this evaluation method for the users to choose the method they want.

        """
        method_pattern = re.compile(r'^eval\d+$')
        methods = [getattr(Keyword, method_name) for method_name in dir(Keyword) if callable(getattr(Keyword, method_name)) and method_pattern.match(method_name)] 
        methods.sort(key=lambda x: x.__name__)
 
        for method in methods:
            docstring = method.__doc__
            if docstring:
                print(f"{method.__name__}:\n{docstring}\n")
        

    def if_there_is(self, ans, keywords):
        for kw in keywords:
            if ans.find(kw.lower()) != -1:
                print(f'keyword:{kw}')
                return True
        return False

