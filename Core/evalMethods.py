from abc import ABC, abstractmethod
from .LLMs import LLMs

class EvalMethods(ABC):
    """Evaluation methods abstract class
    """
    
    def __init__(self, prompt, llm, evalinfo):
        self.prompt = prompt
        self.llm = llm
        self.evalinfo = evalinfo
        self.check()
        
    def check(self):
        """Check if arguments is legal.

        """
        if isinstance(self.prompt, str):
            self.prompt = [self.prompt]
        elif isinstance(self.prompt, list):
            pass
        else:
            raise ValueError(f"{self.prompt} is not a list or str.")
        
        assert(isinstance(self.llm, LLMs)), ValueError(f"llm is not a class of LLM.")
        assert(isinstance(self.evalinfo, dict) or self.evalinfo == None), ValueError(f"Eval info {self.evalinfo} is not right.")
    
    @abstractmethod
    def eval1(self):
        """Evaluation method 1. (At least one)
        """
        pass
    
        