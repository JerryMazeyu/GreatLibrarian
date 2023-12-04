from greatlibrarian.Core import LLMs,FinalScore
from greatlibrarian.Configs import ExampleConfig
from greatlibrarian.Utils import Registry
import dashscope

LLM_base = Registry('LLMs')

@LLM_base.register_module("qwen_turbo")
class new_llm(LLMs):
    def __init__(self,apikey,name,llm_intro):
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro
    
    def get_intro(self):
        return self.llm_intro
    
    def get_name(self):
        return self.name
    
    def __call__(self, prompt: str) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
        model = dashscope.Generation.Models.qwen_turbo,
        prompt = prompt
        )

        if response:
            if response['output']:
                if response['output']['text']:
                    return(response['output']['text'])
        return('API Problem')
    
class FinalScore1 (FinalScore):
     def __init__(self, score_dict,field,threadnum) -> None:
        self.score = score_dict
        self.field = field
        self.threadnum = threadnum

     def get_final_score(self) -> int :
        """

        Used to define the final scoring calculation rules for each testcase.
        The final score is calculated based on the scores from various evalmethods through this rule to obtain the ultimate score.

        """
        if self.score.get('blacklist') is not None and self.score['blacklist'] == 0.0 :
            return(0.0)
        if self.score.get('keywords') is not None and self.score.get('GPT4_eval') is not None:
            if abs(self.score['keywords']-self.score['GPT4_eval']) <= 0.5:
                return(float('%.3f'%((self.score['keywords']+self.score['GPT4_eval'])/2)))
            else:
                return('Human Evaluation')
        if self.score.get('keywords') is not None :
            return(self.score['keywords'])
        if self.score.get('GPT4_eval') is not None:
            return(self.score['GPT4_eval'])

     def final_score_info(self) -> str:
        return (self.get_final_score(),f'The final score of this testcase is {self.get_final_score()}, in {self.field} field.'+f'from thread {self.threadnum}',self.get_final_score())
     


llm_cfg = dict(type='qwen_turbo',apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8", name = "qwen_turbo",llm_intro = '千问\n\n')
qw = LLM_base.build(llm_cfg)
config = ExampleConfig(qw,FinalScore1) 