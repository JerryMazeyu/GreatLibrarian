from greatlibrarian.Core import EvalMethods
from greatlibrarian.Utils import to_list
import warnings
import re
from typing import Tuple


class ToolUse(EvalMethods):
    """Blacklist evaluation"""

    def __init__(self, prompt, ans, evalinfo, field, threadnum) -> None:
        super().__init__(prompt, ans, evalinfo, field, threadnum)
        if not self.evalinfo.get("tool", None):
            warnings.warn("There is no tool usage.", RuntimeWarning)
        self.tools = to_list(self.evalinfo.get("tool"))
        self.methodtotal = 2
        self.field = field

    def getmethodtotal(self) -> int:
        return int((self.methodtotal))

    def set_ans(self, ans) -> None:
        self.ans = ans

    def set_field(self, field) -> None:
        self.field = field

    def set_threadnum(self, threadnum) -> None:
        self.threadnum = threadnum

    def eval1(self) -> float:
        """
        A method for scoring models based on toolUsage.
        Rule:Suppose there are n prompts in total, unit_point = 1/n, for each prompt, the model gets a score of unit_point * (2/3) if it chooses the correct tool, and it gets a score of unit_point * (1/3) if the model sends the correct arguments.
        Returns:
            Score of the model.
        """
        unit_point = 1.0 / len(self.prompt)
        res = 0.0
        for ind, pt in enumerate(self.prompt):
            target_tool = self.tools[ind]["name"]
            target_arg = self.tools[ind]["args"]
            if self.ans[ind].find(f"{target_tool}") != -1:
                res += unit_point * (2 / 3)
            if self.ans[ind].find(f"{target_arg}") != -1:
                res += unit_point * (1 / 3)
        return res

    def eval2(self) -> float:
        """
        A method for scoring models based on toolUsage.
        Rule:Suppose there are n prompts in total, unit_point = 1/n, for each prompt, the model gets a score of unit_point if it both chooses the correct tool and sends the correct arguments.
        Returns:
            Score of the model.
        """
        unit_point = 1.0 / len(self.prompt)
        res = 0.0
        for ind, pt in enumerate(self.prompt):
            target_tool = self.tools[ind]["name"]
            target_arg = self.tools[ind]["args"]
            if (
                self.ans[ind].find(f"{target_tool}") != -1
                and self.ans[ind].find(f"{target_arg}") != -1
            ):
                res += unit_point
        return res

    def score(self, method_num) -> Tuple[float, str]:
        """
        A method for choosing one of the methods in toolUsage to score the model.
        Given a number n and the method will choose the nth eval_method to score the model and print the score.
        The function will return a string like 'The model gets ***{score}*** points in this testcase by toolUsage method.'
        """
        eval_dict = {1: self.eval1, 2: self.eval2}
        eval_method = eval_dict[method_num]
        score = eval_method()
        score_info = (
            f"The model gets {score} points in this testcase by toolUsage method."
        )
        return (score, score_info)

    def showmethod(self) -> None:
        """
        A method to show the methods in this evaluation method for the users to choose the method they want.
        """
        method_pattern = re.compile(r"^eval\d+$")
        methods = [
            getattr(ToolUse, method_name)
            for method_name in dir(ToolUse)
            if callable(getattr(ToolUse, method_name))
            and method_pattern.match(method_name)
        ]
        methods.sort(key=lambda x: x.__name__)

        for method in methods:
            docstring = method.__doc__
            if docstring:
                print(f"{method.__name__}:\n{docstring}\n")
            else:
                print("A method defined by user.")
