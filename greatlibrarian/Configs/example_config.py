from ..Interactor import AutoInteractor
from ..FinalScore import FinalScore1
from abc import ABC


class ExampleConfig(ABC):
    """ExampleConfig abstract class"""

    def __init__(
        self, test_llm, GPT4_eval_llm, finalscore=FinalScore1, interactor=AutoInteractor
    ) -> None:
        self.test_llm = test_llm
        self.GPT4_eval_llm = GPT4_eval_llm
        self.finalscore = finalscore
        self.interactor = interactor
