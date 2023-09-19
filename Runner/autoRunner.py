from Utils import load_from_cfg
from Interactor import AutoInteractor
from TestCase import TestProject
import os
import json
import concurrent.futures
from tqdm import tqdm
from EvalMethods import ToolUse,Keyword,GPT4eval,Blacklist

class AutoRunner():
    def __init__(self, cfg):
        self.cfg = cfg
        load_from_cfg(self, cfg)
        self._check()
        self.load_json()
        
    def _check(self):
        if not hasattr(self, 'llm'):
            raise ValueError("There is no llm in the configure file.")
        if not hasattr(self, 'json_paths'):
            raise ValueError("There is no json_paths in the configure file.")
        if not hasattr(self, 'interactor'):
            print("Find no interactor, default as auto interactor.")
            self.interactor_cls = AutoInteractor
        if not hasattr(self, 'register_agents'):
            print("Find no registered agents, default is empty list.")
            self.interactor = []
    
    def load_json(self):
        self.testprojects = []
        self.json_paths = [os.path.join('TestCase', x) for x in self.json_paths]
        for jsp in self.json_paths:
            with open(jsp) as f:
                jsonobj = json.load(f)
                self.testprojects.append(TestProject(jsonobj))
    
    def run(self):
        """
        Multi-threaded to run each test file to speed things up
        """
        def run_interactor(testproj, interactor_cls, cfg,methodnum):
            for testcase in testproj.get_cases(cfg):
                interactor = interactor_cls(testcase,methodnum)
                # print(interactor.logger_name)
                interactor.run()
                

        methodnum=self.selectmethod()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for testproj in self.testprojects:
                future = executor.submit(run_interactor, testproj, self.interactor_cls, self.cfg,methodnum)
                # log_path=os.path.join('Logs',f"{self.logger_name}.log")
                # score_dict=Getinfo(log_path).get_eval_result()
                # mean_score_info,sum_info=Analyse(score_dict).analyse()

                futures.append(future)

            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
                result = future.result()
    


    def analyse(self):
        """
        The analysis module controls the function,
        the analysis module is the module that makes summary statistics and visualization of the data after evaluation
        """
        pass

    def selectmethod(self):
        """
        A function to record a list, which represents the method that user chooses in each evaluation method.
        The evaluation method that doesn't appear in this testcase will be recorded as 0.
        For example, if the evalstack is like: {"tools":ToolUse,"keywords":Keyword,"blacklist":Blacklist},and the return of the method is [1,2,1,0].
        That means the user chooses method1 in toolUse method, method2 in keyword method and method1 in blacklist method.

        """
        eval_dict={"tool":ToolUse,"keywords":Keyword,"blacklist":Blacklist,"GPT4eval":GPT4eval}
        methodnum=[]
        for key in eval_dict:
                eval_cls=eval_dict[key]
                eval_method=eval_cls('','',{"keywords":["moonlight", "window", "frost", "ground"], "tool":[{"name": "TranslationAPI", "args": "窗前明月光，疑似地上霜。"}]},'')
                print(f'Please choose one of the methods in the {key} evaluation!\nThe methods are shown as below:')
                eval_method.showmethod()
                num=int(input('Please enter the number of your chosen method:'))
                while num>eval_method.getmethodtotal():
                    print("Please input the correct number!")
                    num=int(input('Please enter the number of your chosen method:'))
                methodnum.append(num)
        return(methodnum)