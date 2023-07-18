from Core import Agents

class PromptMarket(Agents):
    def __init__(self) -> None:
        pass
    
    def help(self) -> str:
        temp = """
        Prompt Market: 该工具箱包含了数学、统计的许多语境示例，当你遇到这方面的问题时，它会返回给你一些典型的语境示例，能够帮助你更好的进行上下文学习，但是你需要明确具体的领域，例如：概率论、数理统计等。
        """