from ..Utils import load_from_cfg, record_testcase
from ..Interactor import AutoInteractor,HallucinationInteractor
from ..TestCase import TestProject
import os
import json
import concurrent.futures
from tqdm import tqdm
from ..EvalMethods import ToolUse, Keyword, LLMEval, Blacklist
import threading
from ..Utils import (
    clean_log_dialog,
    to_int,
    record_project_info,
    record_process,
    record_testcase_process,
    setup,
    apply_decorator_to_func,
    generate_logger_subfile,
)
from ..Analyser import Analyse, GetInfo
from ..FinalScore import FinalScore1


class AutoRunner:
    """A class responsible for orchestrating the overall program operation"""

    def __init__(self, **kwargs) -> None:
        self.cfg = kwargs.get('cfg')
        self.path = kwargs.get('path')
        self.project_name = kwargs.get('project_name','')
        self.test_id = kwargs.get('test_id', '0')
        self.test_name = kwargs.get('test_name','')
        self.logs_path = kwargs.get('logs_path','')
        self.test_type = kwargs.get('test_type','common')
        self.testcase_num = 0
        self.logger_path = ""
        self.log_path = ""
        self.testproject_num = 0
        load_from_cfg(self, self.cfg)
        self._check()
        self.load_json()
        self.test_llm_name = self.test_llm.get_name()
        self.LLM_eval_llm_name = self.LLM_eval_llm.get_name()
        self.llm_intro = self.test_llm.get_intro()

    def _check(self) -> None:
        if not hasattr(self, "test_llm"):
            raise ValueError("There is no test_llm in the configure file.")
        # if not hasattr(self, 'json_paths'):
        #     raise ValueError("There is no json_paths in the configure file.")
        if not hasattr(self, "LLM_eval_llm"):
            raise ValueError("There is no LLM_eval_llm in the configure file.")
        # if not hasattr(self, "interactor"):
        #     print("Find no interactor, default as auto interactor.")
        #     self.interactor_cls = AutoInteractor
        if not hasattr(self, "register_agents"):
            print("Find no registered agents, default is empty list.")
            self.register_agents = []
        # if not hasattr(self, "finalscore"):
        #     print("Find no finalscore, default is FinalScore1.")
        #     self.finalscore = FinalScore1
        self.choose_interactor()
        self.testcase_num = self.get_total_testcase()

    def choose_interactor(self) -> None:
        if self.test_type == 'general':
            self.interactor_cls = AutoInteractor
        if self.test_type == 'hallucination':
            self.interactor_cls = HallucinationInteractor

    def load_json(self) -> None:
        self.testprojects = []
        self.json_paths = []
        directory = self.path

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".json"):
                    self.json_paths.append(file_path)
                    self.testproject_num += 1

        for jsp in self.json_paths:
            with open(jsp, encoding="utf-8") as f:
                jsonobj = json.load(f)
                self.testprojects.append(TestProject(jsonobj))
    
    def get_total_testcase(self) -> None:
        directory = self.path
        total_length = 0

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".json"):
                    with open(file_path, encoding="utf-8") as f:
                        jsonobj = json.load(f)
                        if "prompts" in jsonobj:
                            prompts = jsonobj["prompts"]
                            if isinstance(prompts, list):
                                total_length += len(prompts)

        return total_length


    def set_log_file(self):
        if self.logs_path != "":
            self.logs_path = os.path.join(self.logs_path, "Logs")
            if self.test_id == "":
                self.log_path = os.path.join(self.logs_path, generate_logger_subfile(self.logs_path))
            else:
                self.log_path = os.path.join(self.logs_path, self.test_id)
        else:
            if self.test_id == "":
                self.log_path = os.path.join("Logs", generate_logger_subfile(self.logs_path))
            else:
                self.log_path = os.path.join("Logs", self.test_id)

    def run(self) -> None:
        """
        A function enabling parallel execution for each test project.
        """
        self.set_log_file()
        lock = threading.Lock()
        num_done_lock = threading.Lock()
        global num_done
        num_done = 0 
        record_testcase_process(f"目前的进度为：{num_done}/{self.testcase_num}", self.log_path)

        def run_interactor(testproj, interactor_cls, cfg, methodnum, threadnum):
            global num_done
            for testcase in testproj.get_cases(cfg):
                with lock:
                    interactor = interactor_cls(
                        testcase, methodnum, threadnum, self.log_path
                    )
                    dec = setup(logger_name="dialog_init", logger_file=self.log_path)
                    # interactor = apply_decorator_to_all_methods(dec(), interactor)
                    interactor.run = apply_decorator_to_func(dec(), interactor.run)
                    interactor.base_interact = apply_decorator_to_func(
                        dec(), interactor.base_interact
                    )
                    if interactor is not None:
                        interactor.run()
                        with num_done_lock:
                            num_done += 1
                            record_testcase_process(f"目前的进度为：{num_done}/{self.testcase_num}", self.log_path)

            self.logger_path = interactor.get_logger_path()

        method_num = self.selectmethod()
        threadnum = 1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for testproj in self.testprojects:
                future = executor.submit(
                    run_interactor,
                    testproj,
                    self.interactor_cls,
                    self.cfg,
                    method_num,
                    threadnum,
                )
                threadnum += 1

                futures.append(future)

            completed_futures_count = 0
            record_process(
                f"目前的进度为：{completed_futures_count}/{len(futures)}", self.log_path
            )

            for future in tqdm(
                concurrent.futures.as_completed(futures), total=len(futures)
            ):
                result = future.result()
                completed_futures_count += 1
                record_process(
                    f"目前的进度为：{completed_futures_count}/{len(futures)}",
                    self.log_path,
                )
        dec = setup(logger_name="dialog", logger_file=self.log_path)
        mk_clean_log = apply_decorator_to_func(dec(), self.mk_clean_log)
        mk_clean_log(os.path.join(self.log_path, "dialog_init.log"))
        self.analyse(os.path.join(self.log_path, "dialog_init.log"))
        record_project_info(
            self.project_name,
            self.test_llm_name,
            self.LLM_eval_llm_name,
            self.path,
            self.testproject_num,
            self.test_name,
            self.log_path,
        )

    def analyse(self, logger_path) -> None:
        """
        The analysis module controls the function,
        the analysis module is the module that makes summary statistics and visualization of the data after evaluation
        """
        dec = setup(logger_name="analyse", logger_file=self.log_path)
        score_dict = GetInfo(
            os.path.join(self.log_path, "dialog_init.log")
        ).get_eval_result()
        analyse = Analyse(score_dict)
        analyse.analyse = apply_decorator_to_func(dec(), analyse.analyse)
        # analyse = apply_decorator_to_all_methods(dec(), analyse)
        mean_score_info, sum_info, plotinfo = analyse.analyse()
        analyse.report(
            plotinfo,
            self.llm_intro,
            os.path.join(self.log_path, "dialog_init.log"),
            self.log_path,
        )

    def selectmethod(self) -> list[int]:
        """
        A function to record a list, which represents the method that user chooses in each evaluation method.
        The evaluation method that doesn't appear in this testcase will be recorded as 0.
        For example, if the evalstack is like: {"tools":ToolUse,"keywords":Keyword,"blacklist":Blacklist},and the return of the method is [1,2,1,0].
        That means the user chooses method1 in toolUse method, method2 in keyword method and method1 in blacklist method.
        """
        # eval_dict = {
        #     "tool": ToolUse,
        #     "keywords": Keyword,
        #     "blacklist": Blacklist,
        #     "LLMEval": LLMEval,
        # }
        # methodnum = []
        # for key in eval_dict:
        #     eval_cls = eval_dict[key]
        #     eval_method = eval_cls(
        #         "",
        #         "",
        #         {
        #             "keywords": ["moonlight", "window", "frost", "ground"],
        #             "tool": [
        #                 {"name": "TranslationAPI", "args": "窗前明月光，疑似地上霜。"}
        #             ],
        #         },
        #         "",
        #         "",
        #     )
        #     print(
        #         f"Please choose one of the methods in the {key} evaluation!\nThe methods are shown as below:"
        #     )
        #     eval_method.showmethod()
        #     usr_input = input("Please enter the number of your chosen method:")
        #     trans_result = to_int(usr_input)
        #     while trans_result is None or trans_result > eval_method.getmethodtotal():
        #         print(f"Please input a number from 1 to {eval_method.getmethodtotal()}")
        #         usr_input = input("Please enter the number of your chosen method:")
        #         trans_result = to_int(usr_input)

        #     methodnum.append(trans_result)
        # return methodnum
        if self.test_type == 'general':
            methodnum = [1,1,1,1,1]
            return(methodnum)
        
        if self.test_type == 'hallucination':
            methodnum = [1,1,1,2,2]
            return(methodnum)

    def mk_clean_log(self, logger_path) -> None:
        clean_log_dialog(logger_path)
