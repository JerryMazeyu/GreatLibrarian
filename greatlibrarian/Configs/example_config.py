from greatlibrarian.Interactor import AutoInteractor
from greatlibrarian.FinalScore import FinalScore1


class ExampleConfig:
    """ExampleConfig class for users to decide the config of a test."""

    def __init__(
        self, test_llm, LLM_eval_llm, finalscore=FinalScore1, interactor=AutoInteractor
    ) -> None:
        self.test_llm = test_llm
        self.LLM_eval_llm = LLM_eval_llm
        self.finalscore = finalscore
        self.interactor = interactor
