from Core import EvalMethods
from Utils import to_list
import warnings
from LLMs import chatglm_pro

class GPT4eval(EvalMethods):
    def __init__(self, prompt, ans, evalinfo,field):
        super().__init__(prompt, ans, evalinfo,field)
        if not self.evalinfo.get("GPT4eval", None):
            warnings.warn("There is no GPT4eval.", RuntimeWarning)
        self.methodtotal=0
        self.field=field
        self.llm = chatglm_pro
    

    def set_field(self,field):
        self.field=field
    
    def set_ans(self,ans):
        self.ans=ans

        
    def eval1(self):
        """


        """
        pass

    def showmethod(self):
        """
        A method to show the methods in this evaluation method for the users to choose the method they want.

        """
        pass
        

    def getmethodtotal(self):
        return int((self.methodtotal))