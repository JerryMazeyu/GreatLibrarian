from Core import Agents
import getContextExamples as ex
from LLMs.OpenSource import chatglm6b_2

class PromptMarket(Agents):
    def __init__(self) -> None:
        pass
    
    def help(self) -> str:
        # temp = """
        # Prompt Market: 该工具箱包含了数学、统计的许多语境示例，当你遇到这方面的问题时，它会返回给你一些典型的语境示例，能够帮助你更好的进行上下文学习，但是你需要明确具体的领域，例如：概率论、数理统计等。
        # """
        # return temp
        print("PromptMarket User Guide：该工具箱包含了数学、统计的许多语境示例，当你遇到这方面的问题时，它会返回给你一些典型的语境示例，能够帮助你更好的进行上下文学习，但是你需要明确具体的领域，例如：概率论、数理统计等。")
        print("1. Input domain, concept and question, the question is optional.")
        print("2. Input "exit" to quit.")
        print("3. ....")
    
    def __call__(self) -> str:
        while True:
            user_input=input("Please input domain,concept and question(optional)!")
            if user_input.lower()=='exit':
                print("Bye!")
                break
            elif user_input.lower()=="help":
                self.help()
            else:
                prompt=self.process(user_input)
                print("Your prompt is:",prompt)

        
    def process(self,user_input)->str:
        #domain,concept,question=None

        domain=input("Please input knowledge domain:")
        concept=input("Please input concept:")
        question=input("Please input your question(Optional):")
        
        domain,concept,question=user_input

        prompt=ex.get_context_examples(domain,concept,question)
        

        response=chatglm6b_2.__call__(prompt)
        
    


""""

传入domain，返回的promp作为LLM输入进行预设
进行正常的评测，测评内容在domain之内
user在call中调用，call调用process完成识别和预设，识别用正则表达识别出domain，预设需要用LLM接口输入
"""
