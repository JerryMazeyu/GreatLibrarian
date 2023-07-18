from Core import LLMs

class ChatGLM6B(LLMs):
    def __init__(self):
        self.model = "ChatGLM-6B"
        pass
    
    def __call__(self, prompt: str) -> str:
        return "你好，我是ChatGLM6B，很高兴认识你。"

chatglm6b = ChatGLM6B()