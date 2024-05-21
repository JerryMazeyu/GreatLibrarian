from gl.Core import FinalScore


class FinalScore1(FinalScore):
    """A class to decide the final score of a testcase"""

    def __init__(self, score_dict, field, threadnum) -> None:
        self.score = score_dict
        self.field = field
        self.threadnum = threadnum
        self.methodtotal = 2
    
    def getmethodtotal(self) -> int:
        return int((self.methodtotal))

    def get_final_score1(self) -> float:
        """
        Used to define the final scoring calculation rules for each testcase of general type.
        The final score is calculated based on the scores from various evalmethods through this rule to obtain the ultimate score.
        """
        if self.score.get("blacklist") is not None and self.score["blacklist"] == 0.0:
            return 0.0
        if (
            self.score.get("keywords") is not None
            and self.score.get("LLM_eval") is not None
        ):
            if abs(self.score["keywords"] - self.score["LLM_eval"]) <= 0.5:
                return float(
                    "%.3f" % ((self.score["keywords"] + self.score["LLM_eval"]) / 2)
                )
            else:
                return "Human Evaluation"
        if self.score.get("keywords") is not None:
            return self.score["keywords"]
        if self.score.get("LLM_eval") is not None:
            return self.score["LLM_eval"]
        
    def get_final_score2(self) -> float:
        """
        Used to define the final scoring calculation rules for each testcase of hallucination type.
        The final score is calculated based on the scores from various evalmethods through this rule to obtain the ultimate score.
        """
        if self.score.get("LLM_eval") is not None:
            return self.score["LLM_eval"]
        

    def final_score_info(self, method_num) -> str:
        eval_dict = {1: self.get_final_score1, 2:self.get_final_score2}
        eval_method = eval_dict[method_num]
        return (
            eval_method(),
            f"The final score of this testcase is {eval_method()}, in {self.field} field."
            + f"from thread {self.threadnum}",
            eval_method(),
        )
