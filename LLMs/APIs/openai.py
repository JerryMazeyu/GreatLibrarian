from Core import LLMs
import zhipuai

from http import HTTPStatus
import dashscope

class ChatGPT(LLMs):
    def __init__(self):
        self.apikey = ""
        self.name = "gpt-3.5-turbo"
    
    def __call__(self, prompt: str) -> str:
        pass

class chatglm_pro(LLMs):
    def __init__(self):
        self.apikey = "450fe9e4faec64c0a48234a5d92115ef.aWoqpjlhWO2Kpbvw"
        self.name = "chatglm_pro"
    
    def __call__(self, prompt: str) -> str:
        zhipuai.api_key = self.apikey
        response = zhipuai.model_api.invoke(
        model="chatglm_pro",
        prompt=[{"role": "user", "content": prompt}],
        top_p=0.7,
        temperature=0.9,
        )
        if response['code']==200:
            return(response['data']['choices'][0]['content'])
        else:
            return('API Problem')

class qwen_turbo(LLMs):
    def __init__(self):
        self.apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8"
        self.name = "qwen_turbo"
    
    def __call__(self, prompt: str) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt
        )

        if response['status_code'].value==200:
            return(response['output']['text'])
        else:
            return('API Problem')

chatgpt = ChatGPT()