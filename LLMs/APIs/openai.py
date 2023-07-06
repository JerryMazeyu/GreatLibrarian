from Core import LLMs

class ChatGPT(LLMs):
    def __init__(self):
        self.apikey = ""
        self.name = "gpt-3.5-turbo"
    
    def __call__(self, prompt: str) -> str:
        pass

chatgpt = ChatGPT()