import os
from ..Utils import (
    clean_log_dialog,
    append_log,
    clear_logs,
    load_from_cfg,
    generate_logger_subfile,
    setup,
    apply_decorator_to_func,
)
from ..Analyser import Analyse, GetInfo


class UpdateRunner:
    """A class responsible for orchestrating the overall program operation"""

    def __init__(self, cfg, Test_ID) -> None:
        self.cfg = cfg
        self.Test_ID = Test_ID
        self.log_dir = ""
        load_from_cfg(self, cfg)
        self._check()
        self.test_llm_name = self.test_llm.get_name()
        self.LLM_eval_llm_name = self.LLM_eval_llm.get_name()
        self.llm_intro = self.test_llm.get_intro()

    def _check(self) -> None:
        if not hasattr(self, "test_llm"):
            raise ValueError("There is no test_llm in the configure file.")
        if not hasattr(self, "LLM_eval_llm"):
            raise ValueError("There is no LLM_eval_llm in the configure file.")
        if not hasattr(self, "Test_ID"):
            raise ValueError("There is no Test_ID in the configure file.")

    def run(self) -> None:
        Test_ID = self.Test_ID
        if Test_ID == "":
            Test_ID_dir = generate_logger_subfile()
        else:
            Test_ID_dir = Test_ID
        self.log_dir = os.path.join("Logs", Test_ID_dir)
        source_log_path = os.path.join(self.log_dir, "human_evaluation.log")
        destination_log_path = os.path.join(self.log_dir, "dialog_init.log")
        append_log(source_log_path, destination_log_path)
        clear_logs(os.path.join(self.log_dir, "dialog.log"))
        clear_logs(os.path.join(self.log_dir, "analyse.log"))

        dec = setup(logger_name="dialog", logger_file=self.log_dir)
        mk_clean_log = apply_decorator_to_func(dec(), self.mk_clean_log)
        mk_clean_log(os.path.join(self.log_dir, "dialog_init.log"))
        self.analyse(destination_log_path)

    def analyse(self, logger_path) -> None:
        """
        The analysis module controls the function,
        the analysis module is the module that makes summary statistics and visualization of the data after evaluation
        """
        dec = setup(logger_name="analyse", logger_file=self.log_dir)
        analyse = Analyse(score_dict)
        analyse.analyse = apply_decorator_to_func(dec(), analyse.analyse)
        score_dict = GetInfo(logger_path).get_eval_result()
        mean_score_info, sum_info, plotinfo = analyse.analyse()
        analyse.report(
            plotinfo, self.llm_intro, logger_path, os.path.join("Logs", self.Test_ID)
        )

    def mk_clean_log(self, logger_path) -> None:
        clean_log_dialog(logger_path)
