from ..Utils import load_from_cfg
from ..Interactor import AutoInteractor
from ..TestCase import TestProject
import os
import json
import concurrent.futures
from tqdm import tqdm
from ..EvalMethods import ToolUse, Keyword, GPT4eval, Blacklist
import threading
from ..Utils import clean_log_dialog, to_int, record_project_info, record_process
from ..Analyser import Analyse, Getinfo
from ..FinalScore import FinalScore1


class AutoRunner:
    """A class responsible for orchestrating the overall program operation"""

    def __init__(self, cfg, path, project_name) -> None:
        self.path = path
        self.cfg = cfg
        self.testproject_num = 0
        self.project_name = project_name
        load_from_cfg(self, cfg)
        self._check()
        self.load_json()
        # llm = self.llm
        self.test_llm_name = self.test_llm.get_name()
        self.GPT4_eval_llm_name = self.GPT4_eval_llm.get_name()
        self.llm_intro = self.test_llm.get_intro()

    def _check(self) -> None:
        if not hasattr(self, "test_llm"):
            raise ValueError("There is no test_llm in the configure file.")
        # if not hasattr(self, 'json_paths'):
        #     raise ValueError("There is no json_paths in the configure file.")
        if not hasattr(self, "GPT4_eval_llm"):
            raise ValueError("There is no GPT4_eval_llm in the configure file.")
        if not hasattr(self, "interactor"):
            print("Find no interactor, default as auto interactor.")
            self.interactor_cls = AutoInteractor
        if not hasattr(self, "register_agents"):
            print("Find no registered agents, default is empty list.")
            self.register_agents = []
        if not hasattr(self, "finalscore"):
            print("Find no finalscore, default is FinalScore1.")
            self.finalscore = FinalScore1

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

    def run(self) -> None:
        """
        A function enabling parallel execution for each test project.
        """
        lock = threading.Lock()

        def run_interactor(testproj, interactor_cls, cfg, methodnum, threadnum):
            for testcase in testproj.get_cases(cfg):
                with lock:
                    interactor = interactor_cls(testcase, methodnum, threadnum)
                    if interactor is not None:
                        interactor.run()
            global logger_path
            logger_path = interactor.get_logger_path()

        method_num = self.selectmethod()
        threadnum = 1

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for testproj in self.testprojects:
                future = executor.submit(
                    run_interactor,
                    testproj,
                    self.interactor,
                    self.cfg,
                    method_num,
                    threadnum,
                )
                threadnum += 1

                futures.append(future)

            completed_futures_count = 0
            record_process(f"目前的进度为：{completed_futures_count}/{len(futures)}")

            for future in tqdm(
                concurrent.futures.as_completed(futures), total=len(futures)
            ):
                result = future.result()
                completed_futures_count += 1
                record_process(
                    f"目前的进度为：{completed_futures_count}/{len(futures)}"
                )

        self.mk_clean_log(logger_path)
        self.analyse(logger_path)
        record_project_info(
            self.project_name,
            self.test_llm_name,
            self.GPT4_eval_llm_name,
            self.path,
            self.testproject_num,
        )

    def analyse(self, logger_path) -> None:
        """
        The analysis module controls the function,
        the analysis module is the module that makes summary statistics and visualization of the data after evaluation
        """

        score_dict = Getinfo(logger_path).get_eval_result()
        print(score_dict)
        analyse = Analyse(score_dict)
        mean_score_info, sum_info, plotinfo = analyse.analyse()
        analyse.report(plotinfo, logger_path, self.llm_intro)

    def selectmethod(self) -> list[int]:
        """
        A function to record a list, which represents the method that user chooses in each evaluation method.
        The evaluation method that doesn't appear in this testcase will be recorded as 0.
        For example, if the evalstack is like: {"tools":ToolUse,"keywords":Keyword,"blacklist":Blacklist},and the return of the method is [1,2,1,0].
        That means the user chooses method1 in toolUse method, method2 in keyword method and method1 in blacklist method.
        """
        eval_dict = {
            "tool": ToolUse,
            "keywords": Keyword,
            "blacklist": Blacklist,
            "GPT4eval": GPT4eval,
        }
        methodnum = []
        for key in eval_dict:
            eval_cls = eval_dict[key]
            eval_method = eval_cls(
                "",
                "",
                {
                    "keywords": ["moonlight", "window", "frost", "ground"],
                    "tool": [
                        {"name": "TranslationAPI", "args": "窗前明月光，疑似地上霜。"}
                    ],
                },
                "",
                "",
            )
            print(
                f"Please choose one of the methods in the {key} evaluation!\nThe methods are shown as below:"
            )
            eval_method.showmethod()
            usr_input = input("Please enter the number of your chosen method:")
            trans_result = to_int(usr_input)
            while trans_result is None or trans_result > eval_method.getmethodtotal():
                print(f"Please input a number from 1 to {eval_method.getmethodtotal()}")
                usr_input = input("Please enter the number of your chosen method:")
                trans_result = to_int(usr_input)

            methodnum.append(trans_result)
        return methodnum

    def mk_clean_log(self, logger_path) -> None:
        clean_log_dialog(logger_path)
