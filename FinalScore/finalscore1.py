from Core import FinalScore

class FinalScore1 (FinalScore):
     def __init__(self, score_dict,field) -> None:
        self.score = score_dict
        self.field = field

     def get_final_score(self) -> int :
        if self.score.get('blacklist') is not None and self.score['blacklist'] == 0.0 :
            return(0.0)
        if self.score.get('keywords') is not None and self.score.get('GPT4_eval') is not None:
            if abs(self.score[keywords]-self.score['GPT4_eval']) > 0.5:
                return(float('%.3f'%((self.score[keywords]+self.score['GPT4_eval'])/2)))
            else:
                return('Human Evaluation')
        if self.score.get('keywords') is not None :
            return(self.score['keywords'])
        if self.score.get('GPT4_eval') is not None:
            return(self.score['GPT4_eval'])
     def final_score_info(self) -> str:
        return (self.get_final_score(),f'The final score of this testcase is {self.get_final_score()}, in {self.field} field.')

