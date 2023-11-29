from greatlibrarian.Core import LLMs,FinalScore
from greatlibrarian.Configs import ExampleConfig
import dashscope

class new_llm(LLMs):
    def __init__(self):
        self.apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8"
        self.name = "qwen_turbo"
        self.llm_intro = "通义千问是由阿里巴巴集团开发的一款人工智能语言模型应用，它采用了大规模机器学习技术，能够模拟人类自然语言的能力，提供多种服务，如文本翻译、聊天机器人、\n\n自动回复、文档摘要等。\n\n它的核心特点是多轮对话，可以理解用户的意图并进行有效的回复；同时，它还具有强大的文案创作能力，可以为用户提供优秀的文字创意，比如续写小说、撰写邮件等。\n\n此外，通义千问还具备多模态的知识理解能力，可以识别图片、音频、视频等多种媒体形式，并从中提取出关键信息。不仅如此，通义千问还支持多语言，可以实现中文、\n\n英文等不同语言之间的自由转换。\n\n目前，通义千问正在接受内测阶段，并已在各大手机应用市场上线，所有人都可以通过APP直接体验最新模型能力。\n\n"
    
    def get_intro(self):
        return self.llm_intro
    
    def __call__(self, prompt: str) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
        model = dashscope.Generation.Models.qwen_turbo,
        prompt=prompt
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
        

config = ExampleConfig(new_llm,FinalScore1) 