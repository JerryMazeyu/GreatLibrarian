from abc import ABC, abstractmethod


class FinalScore(ABC):
    """FinalScore abstract class"""

    def __init__(self, score_dict, field, threadnum) -> None:
        self.score = score_dict
        self.field = field
        self.threadnum = threadnum

    def final_score_info(self) -> str:
        """
        Return:
            The finalscore information of the testcase.
        """

        return f"The final score of this testcase is {self.get_final_score()}, in {self.field} field."