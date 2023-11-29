from greatlibrarian.Utils import Registry
import dashscope

LLMS = Registry('LLMs')

@LLMS.register_module("qwen_turbo")
class qwen_turbo():
    def __init__(self,apikey="sk-9ca2ad73e7d34bd4903eedd6fc70d0d8",name="qwen_turbo"):
        self.apikey = apikey
        self.name = name
    
    def __call__(self, prompt: str) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt=prompt
        )

        if response:
            if response['output']:
                if response['output']['text']:
                    return(response['output']['text'])
        return('API Problem')

print(LLMS)



#type 即注册时装饰器传入的name
llm_cfg = dict(type='qwen_turbo',apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8", name = "qwen_turbo")


wx = LLMS.build(llm_cfg)
print(type(wx))

print(wx.apikey)
print(wx.name)

a=wx('世界最高峰是')
print(a)