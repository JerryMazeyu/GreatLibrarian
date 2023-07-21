from Core import Agents

class PromptMarket(Agents):
    def __init__(self) -> None:
        pass
    
    def help(self) -> str:
        temp = """
        Prompt Market: 该工具箱包含了数学、统计的许多语境示例，当你遇到这方面的问题时，它会返回给你一些典型的语境示例，能够帮助你更好的进行上下文学习，但是你需要明确具体的领域，例如：概率论、数理统计等。
        """
        return temp
    
    def __call__(self, prompt: str) -> str:
        pass
    
    def process(self, sql):
        pass
    
    def help(self):
        pass

""""

传入domain，返回的promp作为LLM输入进行预设
进行正常的评测，测评内容在domain之内
user在call中调用，call调用process完成识别和预设，识别用正则表达识别出domain，预设需要用LLM接口输入
"""