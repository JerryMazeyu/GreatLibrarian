from abc import ABC, abstractmethod

class FinalScore (ABC):

    """
    FinalScore abstract class
    """
    
    def __init__(self, score_dict,field) -> None:
        self.score = score_dict
        self.field = field

    @abstractmethod
    def get_final_score(self) -> int :

        """
        The rule to determine the final score of a testcase based by the score of every evalmethod.
        Return:
            the final score of the testcase
        """
        pass
        
    def final_score_info(self) -> str:

        """
        Return:
            The finalscore information of the testcase.
        """

        return (f'The final score of this testcase is {self.get_final_score()}, in {self.field} field.') 
               

