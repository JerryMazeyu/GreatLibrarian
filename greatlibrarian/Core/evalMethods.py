from abc import ABC, abstractmethod
from greatlibrarian.Utils import to_list


class EvalMethods(ABC):
    """Evaluation methods abstract class"""

    def __init__(self, prompt, ans, evalinfo, field, threadnum) -> None:
        self.prompt = prompt
        self.ans = ans
        self.evalinfo = evalinfo
        self.methods = []
        self.field = field
        self.threadnum = threadnum
        self.check()

    def check(self) -> None:
        """
        Check if arguments is legal.
        If there is any eval method implementation, use eval<xxx> as the function name.
        """
        self.prompt = to_list(self.prompt)
        self.ans = to_list(self.ans)
        assert isinstance(self.evalinfo, dict) or self.evalinfo is None, ValueError(
            f"Eval info {self.evalinfo} is not right."
        )

    @abstractmethod
    def eval1(self) -> float:
        """
        Evaluation method 1. (At least one)
        """
        pass

    @classmethod
    def get_eval_name(cls) -> str:
        return [
            method_name
            for method_name in dir(cls)
            if callable(getattr(cls, method_name))
            if method_name.startswith("eval")
        ]
