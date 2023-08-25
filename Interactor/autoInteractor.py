from typing import Any
from Utils import add_logger_to_class,load_from_cfg
from Recoder import Recoder
from EvalMethods import ToolUse,Keyword,GPT4eval,Blacklist

@add_logger_to_class
class AutoInteractor():
    def __init__(self, testcase) -> None:
        load_from_cfg(self, testcase)
        # self.recoders = []

    
    def eval(self):
        """
        A function that creates a evaluation stack for every testcase.
        This function uses a dictionary to judge whether a evaluation method should be used in this testcase, and it's certain that this method should be used, it will be added to a dictionary. 
        The dictionary "eval_stack" is the final evaluation stack, the value of every key is the corresponding evaluation object.

        """
        eval_dict={"tools":ToolUse,"keywords":Keyword,"blacklist":Blacklist,"GPT4eval":GPT4eval}
        eval_stack={}
        for key in eval_dict.keys():
            if (key in self.raw_eval_info.keys()):
                eval_cls=eval_dict[key]
                eval_method=eval_cls(self.prompt,'',self.raw_eval_info)
                eval_stack[key]=eval_method
        return(eval_stack)

    def base_interact(self, prompt):

        """
        A function to create the interaction between the LLM and the user.
        It will record the dialogue in the log file and the answers to prompts sent to LLM from the LLM will be saved in a list called ans_list.
        In this method, the dialogue mainly contains the propmts that the user sends to LLM, and the response from the LLM.

        """
        # recoder = Recoder()
        # recoder.ind = ind
        print(f"---------- New Epoch ----------")
        ans_list=[]
        for ind, pr in enumerate(prompt):
            # recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr}")
            # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.llm(pr)
            print(f"To User:\t {ans}")
            ans_list.append(ans)
        return(ans_list)


        # recoder.dialoge[ind] += f"To User:\t {ans}"
        # self.recoders.append(recoder)
    
    def tool_interact(self, prompt, tools:list):

        """
        A function to create the interaction between the LLM, the user and the tool.
        It will record the dialogue in the log file and the content that LLM sends to the tool will be saved in a list called ans_list.
        In this method, the dialogue mainly contains the propmts that the user sends to LLM, the content that the LLM sends to the tool and the response from the tool.

        """
        # recoder = Recoder()
        # recoder.ind = ind
        # recoder.prompt = prompt
        print(f"---------- New Epoch ----------")
        ans_list=[]
        for ind, pr in enumerate(prompt):
            # recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr}")
            # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.llm(pr)
            ans_list.append(ans)
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
        return(ans_list)
    

    def selectmethod(self):#TODO:这个方法暂时不确定后续应该放在哪里，因为并行可能导致该函数重复运行不必要的次数，先临时写在这个地方
        """
        A function to record a list, which represents the method that user chooses in each evaluation method.
        The evaluation method that doesn't appear in this testcase will be recorded as 0.
        For example, if the evalstack is like: {"tools":ToolUse,"keywords":Keyword,"blacklist":Blacklist},and the return of the method is [1,2,1,0].
        That means the user chooses method1 in toolUse method, method2 in keyword method and method1 in blacklist method.

        """
        eval_dict={"tools":ToolUse,"keywords":Keyword,"blacklist":Blacklist,"GPT4eval":GPT4eval}
        methodnum=[]
        for key in eval_dict:
            if (key in self.raw_eval_info.keys()):
                eval_cls=eval_dict[key]
                eval_method=eval_cls(self.prompt,'',self.raw_eval_info)
                print(f'Please choose one of the methods in the {key} evaluation!\nThe methods are shown as below:')
                eval_method.showmethod()
                num=int(input('Please enter the number of your chosen method:'))
                while num>eval_method.getmethodtotal():
                    print("Please input the correct number!")
                    num=int(input('Please enter the number of your chosen method:'))
                methodnum.append(num)
            else:
                methodnum.append(0)
        return(methodnum)

    
    def run(self):

        """
        A function to start the interaction.
        If the interaction contains tools, it will record the dialogue between the tool, the user and the LLM.
        If the interaction doesn't contain tools, it will record the dialogue between the user and the LLM.
        The function use a list to record the answers from the LLM, and use this answer list to evaluate the LLM in this testcase. It will evaluate the LLM with every method chosen by the user.
        
        """
        methodnum=self.selectmethod()#TODO:也是临时放在这里
        eval_stack=self.eval()
        if self.eval_info.get('tool', None):
            toolusage_ans=self.tool_interact(self.prompt, self.eval_info['tool'])
            eval_obj=eval_stack['tools']
            eval_obj.set_ans(toolusage_ans)
            _,tool_eval_info=eval_obj.score(methodnum[0]) 
        else:
            keywords_ans=self.base_interact(self.prompt)
            eval_obj=eval_stack['keywords']
            eval_obj.set_ans(keywords_ans)
            _,keywords_eval_info=eval_obj.score(methodnum[1]) 
            print(keywords_eval_info)
            if  self.eval_info.get('blacklist', None):
                eval_obj=eval_stack['blacklist']
                eval_obj.set_ans(keywords_ans)
                _,blacklist_eval_info=eval_obj.score(methodnum[2]) 
                print(blacklist_eval_info)
                print(GPT4_eval_info)
            if  self.eval_info.get('GPT4eval', None):
                eval_obj=eval_stack['GPT4eval']
                eval_obj.set_ans(keywords_ans)
                _,GPT4_eval_info=eval_obj.score(methodnum[3]) 
                print(GPT4_eval_info)


case=[{ 'eval_info': {"keywords":["yes", "same"],"blacklist":['no']}}]
test=AutoInteractor(case)
test.run()

