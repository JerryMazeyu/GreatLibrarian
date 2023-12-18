from ..Core import EvalMethods
import warnings
import re
from typing import Tuple


class GPT4eval(EvalMethods):
    """Blacklist evaluation"""

    def __init__(self, prompt, ans, evalinfo, field, threadnum) -> None:
        super().__init__(prompt, ans, evalinfo, field, threadnum)
        if not self.evalinfo.get("GPT4eval", None):
            warnings.warn("There is no GPT4eval.", RuntimeWarning)
        self.methodtotal = 1
        self.field = field

    def set_llm(self, llm) -> None:
        self.llm = llm

    def set_field(self, field) -> None:
        self.field = field

    def set_ans(self, ans) -> None:
        self.ans = ans

    def set_prompt(self, prompt) -> None:
        self.prompt = prompt

    def set_threadnum(self, threadnum) -> None:
        self.threadnum = threadnum

    def eval1(self) -> float:
        """
        Give the GPT4 this testcase and the answer from the LLM being tested, let GPT4 give a score from 0-1.
        The prompt given to the GPT4 is like this:
        "Next, I will give you a question and an answer. Please rate this answer on a scale from 0 to 1, with 1 being the highest score and 0 being the lowest score.
        Please provide a score with one decimal place of precision as output, and only output this score, without any other information. Here is the question and answer information:
        Question: {The question for this testcase};
        Answer: {The answer provided by the evaluated LLM}.
        Please rate this answer: "
        """
        input = f"Next, I will give you a question and an answer. Please rate this answer on a scale from 0 to 1, with 1 being the highest score and 0 being the lowest score.\n Please provide a score with one decimal place of precision as output, and only output this score, without any other information or punctuation marks. Here is the question and answer information:\nQuestion：{self.prompt};\nAnswer：{self.ans};\nPlease rate this answer:"
        output = self.llm(input)
        float_pattern = r"[-+]?\d*\.\d+"
        match = re.search(float_pattern, output)
        if match:
            score = float(match.group())
        return score

    def score(self, method_num) -> Tuple[float, str]:
        """
        A method for choosing one of the methods in GPT4eval to score the model.
        Given a number n and the method will choose the nth eval_method to score the model and print the score. (the number n starts from 1)
        The function will return a string like 'The model gets ***{score}*** points in this testcase by GPT4eval method.'
        """
        eval_dict = {1: self.eval1}
        eval_method = eval_dict[method_num]
        score = eval_method()
        score_info = f"The model gets {score} points in this testcase by GPT4eval method, in {self.field} field."
        return (score, score_info)

    def showmethod(self) -> None:
        """
        A method to show the method in this evaluation method.
        """
        method_pattern = re.compile(r"^eval\d+$")
        methods = [
            getattr(GPT4eval, method_name)
            for method_name in dir(GPT4eval)
            if callable(getattr(GPT4eval, method_name))
            and method_pattern.match(method_name)
        ]
        methods.sort(key=lambda x: x.__name__)

        for method in methods:
            docstring = method.__doc__
            if docstring:
                print(f"{method.__name__}:\n{docstring}\n")
            else:
                print("A method defined by user.")

    def getmethodtotal(self) -> int:
        return int((self.methodtotal))
