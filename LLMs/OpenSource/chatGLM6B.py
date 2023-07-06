from Core import LLMs

class ChatGLM6B(LLMs):
    def __init__(self):
        self.model = "ChatGLM-6B"
        pass
    
    def __call__(self, prompt: str) -> str:
        pass

chatglm6b = ChatGLM6B()