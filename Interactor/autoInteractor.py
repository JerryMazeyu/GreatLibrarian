from typing import Any
from Utils import add_logger_to_class, load_from_cfg
from Recoder import Recoder

@add_logger_to_class
class AutoInteractor():
    def __init__(self, testcase) -> None:
        load_from_cfg(self, testcase)
        # self.recoders = []
    
    def base_interact(self, prompt):
        # recoder = Recoder()
        # recoder.ind = ind
        print(f"---------- New Epoch ----------")
        for ind, pr in enumerate(prompt):
            # recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr}")
            # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.llm(pr)
            print(f"To User:\t {ans}")
            # recoder.dialoge[ind] += f"To User:\t {ans}"
        # self.recoders.append(recoder)
    
    def tool_interact(self, prompt, tools:list):
        # recoder = Recoder()
        # recoder.ind = ind
        # recoder.prompt = prompt
        print(f"---------- New Epoch ----------")
        for ind, pr in enumerate(prompt):
            # recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr}")
            # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.llm(pr)
            if ans.find(tools[0].name) != -1:  # TODO: add multi tools
                # recoder.tools = tools[0].name
                print(f"To Tool:\t {ans}")
                # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
                tool_response = self.tools[0](ans)
                print(f"To LLM:\t {tool_response}")
                # recoder.dialoge[ind] += f"To LLM:\t {tool_response}\n"
                ans = self.llm(tool_response)
            print(f"To User:\t {ans}")
        #     recoder.dialoge[ind] += f"To LLM:\t {tool_response}\n"
        # self.recoders.append(recoder)
    
    def run(self):
        if self.eval_info.get('tool', None):
            self.tool_interact(self.prompt, self.eval_info['tool'])
        else:
            self.base_interact(self.prompt)


    
        

