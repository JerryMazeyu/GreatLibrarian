from typing import Any
from Core import Runner
from Utils import add_logger
from Recoder import Recoder

@add_logger(logger_file='Logs')
class AutoInteractor(Runner):
    def __init__(self, cfg) -> None:
        super().__init__(cfg)
        self.recoders = []
        
    def base_interact(self, ind, prompt):
        recoder = Recoder()
        recoder.ind = ind
        print(f"---------- Epoch [{ind}] ----------")
        for ind, pr in enumerate(prompt):
            recoder.dialoge[ind] = ''
            print(f"To LLM:\t {prompt}")
            recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.llm(pr)
            print(f"To User:\t {ans}")
            recoder.dialoge[ind] += f"To User:\t {ans}"
        self.recoders.append(recoder)
    
    def tool_interact(self, ind, prompt, tools:list):
        recoder = Recoder()
        recoder.ind = ind
        recoder.prompt = prompt
        print(f"---------- Epoch [{ind}] ----------")
        for ind, pr in enumerate(prompt):
            recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr}")
            recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.llm(pr)
            if ans.find(tools[0].name) != -1:  # TODO: add multi tools
                recoder.tools = tools[0].name
                print(f"To Tool:\t {ans}")
                recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
                tool_response = self.tools[0](ans)
                print(f"To LLM:\t {tool_response}")
                recoder.dialoge[ind] += f"To LLM:\t {tool_response}\n"
                ans = self.llm(tool_response)
            print(f"To User:\t {ans}")
            recoder.dialoge[ind] += f"To LLM:\t {tool_response}\n"
        self.recoders.append(recoder)
    
    def run(self):
        pass



    
        

