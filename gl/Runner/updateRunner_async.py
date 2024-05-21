import os
from gl.Utils import (
    clean_log_dialog_async,
    append_log,
    clear_logs,
    load_from_cfg,
    generate_logger_subfile,
    setup_async,
    apply_decorator_to_func_async,
)
from gl.Analyser import Analyse, GetInfo


class UpdateRunner_Async:
    """A class responsible for orchestrating the overall program operation"""

    def __init__(self, **kwargs) -> None:
        self.cfg = kwargs.get('cfg')
        self.Test_ID = kwargs.get('Test_ID')
        self.log_dir = kwargs.get('log_dir')
        self.test_type = kwargs.get('test_type')
        load_from_cfg(self, self.cfg)
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

    async def run(self) -> None:
        Test_ID = self.Test_ID
        # if Test_ID == "":
        #     Test_ID_dir = generate_logger_subfile()
        # else:
        Test_ID_dir = Test_ID
        self.log_dir = os.path.join(self.log_dir, 'Logs')
        self.log_dir = os.path.join(self.log_dir, Test_ID)
        # self.log_dir = os.path.join("Logs", Test_ID_dir)
        source_log_path = os.path.join(self.log_dir, "human_evaluation.log")
        destination_log_path = os.path.join(self.log_dir, "dialog_init.log")
        append_log(source_log_path, destination_log_path)
        await clear_logs(os.path.join(self.log_dir, "dialog.log"))
        await clear_logs(os.path.join(self.log_dir, "analyse.log"))

        dec = await setup_async(logger_name="dialog", logger_file=self.log_dir)
        mk_clean_log = await apply_decorator_to_func_async(dec(), self.mk_clean_log)
        await mk_clean_log(os.path.join(self.log_dir, "dialog_init.log"))
        await self.analyse(destination_log_path)

    async def analyse(self, logger_path) -> None:
        """
        The analysis module controls the function,
        the analysis module is the module that makes summary statistics and visualization of the data after evaluation
        """
        score_dict = GetInfo(logger_path).get_eval_result()
        dec = await setup_async(logger_name="analyse", logger_file=self.log_dir)
        analyse = Analyse(score_dict)
        analyse.analyse = await apply_decorator_to_func_async(dec(), analyse.analyse)
        mean_score_info, sum_info, plotinfo = await analyse.analyse()
        analyse.report(plotinfo, self.llm_intro, logger_path, self.log_dir, self.test_type)

    async def mk_clean_log(self, logger_path) -> None:
        await clean_log_dialog_async(logger_path)
