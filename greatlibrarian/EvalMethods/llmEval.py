from ..Core import EvalMethods
import warnings
import re
from typing import Tuple
import warnings


class LLMEval(EvalMethods):
    """Blacklist evaluation"""

    def __init__(self, prompt, ans, evalinfo, field, threadnum) -> None:
        super().__init__(prompt, ans, evalinfo, field, threadnum)
        if not self.evalinfo.get("LLMEval", None):
            warnings.warn("There is no LLMEval.", RuntimeWarning)
        self.methodtotal = 1
        self.field = field
        self.groud_truth = self.evalinfo["keywords"]

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
        score = 0.5
        input = f"接下来，我将给您一个问题、一个回答以及问题的标准答案。请严格以标准答案为参照，判断给出对于该问题的回答是否正确，然后在0到1的范围内对此回答进行评分，其中1表示最高分，0表示最低分。请以一位小数的精度提供评分，若您认为回答正确则分数大于0.5，错误则小于等于0.5。只输出评分，不包含任何其他信息或标点符号。以下是问题和答案的信息：问题：{self.prompt};回答：{self.ans};标准答案：{self.groud_truth}。请严格参照标准答案对针对该问题的回答进行评分："
        #input = f"接下来，我将给您一个问题、一个回答以及问题的标准答案。请根据问题、回答以及标准答案在0到1的范围内对此回答进行评分，其中1表示最高分，0表示最低分。请以一位小数的精度提供评分，若您认为回答正确则分数大于0.5，错误则小于等于0.5。只输出评分，不包含任何其他信息或标点符号。以下是问题、回答以及标准答案的信息：问题：{self.prompt};回答：{self.ans};标准答案：{self.groud_truth}。请对此回答进行评分："
        output = self.llm(input)
        float_pattern = r"[-+]?\d*\.\d+"
        try:
            match = re.search(float_pattern, output)
        except Exception as e:
            warning_message = f"Warning: An re exception occurred - {e}"
            warnings.warn(warning_message, RuntimeWarning)
        if match:
            score = float(match.group())
        return score

    def score(self, method_num) -> Tuple[float, str]:
        """
        A method for choosing one of the methods in LLMEval to score the model.
        Given a number n and the method will choose the nth eval_method to score the model and print the score. (the number n starts from 1)
        The function will return a string like 'The model gets ***{score}*** points in this testcase by LLMEval method.'
        """
        eval_dict = {1: self.eval1}
        eval_method = eval_dict[method_num]
        score = eval_method()
        score_info = f"The model gets {score} points in this testcase by LLMEval method, in {self.field} field."
        return (score, score_info)

    def showmethod(self) -> None:
        """
        A method to show the method in this evaluation method.
        """
        method_pattern = re.compile(r"^eval\d+$")
        methods = [
            getattr(LLMEval, method_name)
            for method_name in dir(LLMEval)
            if callable(getattr(LLMEval, method_name))
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
