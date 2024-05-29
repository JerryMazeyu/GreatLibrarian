from gl.Utils import (
    load_from_cfg,
    human_evaluation,
    setup,
    apply_decorator_to_func,
)
from gl.EvalMethods import ToolUse, Keyword, LLMEval, Blacklist
import warnings
from gl.FinalScore import FinalScore1

class SafetyInteractor:
    """A class to keep the interaction between the LLM and GreatLibrarian"""

    def __init__(self, testcase, methodnum, threadnum, logger_path="") -> None:
        load_from_cfg(self, testcase)
        # self.recoders = []
        self.methodnum = methodnum
        self.threadnum = threadnum
        self.logger_path = logger_path
        self.human_evaluation = human_evaluation

    def eval(self) -> dict:
        """
        A function that creates a evaluation stack for every testcase.
        This function uses a dictionary to judge whether a evaluation method should be used in this testcase, and it's certain that this method should be used, it will be added to a dictionary.
        The dictionary "eval_stack" is the final evaluation stack, the value of every key is the corresponding evaluation object.
        """
        eval_dict = {
            "tool": ToolUse,
            "keywords": Keyword,
            "blacklist": Blacklist,
            "LLMEval": LLMEval,
        }
        eval_stack = {}
        for key in eval_dict.keys():
            if key in self.eval_info.keys():
                eval_cls = eval_dict[key]
                eval_method = eval_cls(self.prompt, "", self.eval_info, "", 0)
                eval_stack[key] = eval_method
        return eval_stack

    def get_logger_path(self) -> str:
        return self.logger_path

    def base_interact(self, prompt) -> list:
        """
        A function to create the interaction between the LLM and the user.
        It will record the dialogue in the log file and the answers to prompts sent to LLM from the LLM will be saved in a list called ans_list.
        In this method, the dialogue mainly contains the propmts that the user sends to LLM, and the response from the LLM.
        """
        # recoder = Recoder()
        # recoder.ind = ind

        print(f"---------- New Epoch ---------- from thread {self.threadnum}")
        for ind, pr in enumerate(prompt):
            # recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr} from thread {self.threadnum}")
            # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.test_llm(pr)
            # ans = "Yes"
            print(f"To User:\t {ans} from thread {self.threadnum}")

            try:
                ans = ans.lower()
            except Exception as e:
                warning_message = f"Warning: An API exception occurred - {e}"
                warnings.warn(warning_message, RuntimeWarning)
                ans = ans 

        return ans

    def run(self) -> None:
        """
        A function to start the interaction.
        If the interaction contains tools, it will record the dialogue between the tool, the user and the LLM.
        If the interaction doesn't contain tools, it will record the dialogue between the user and the LLM.
        The function use a list to record the answers from the LLM, and use this answer list to evaluate the LLM in this testcase. It will evaluate the LLM with every method chosen by the user.
        """
        score_dict = {}
        ans= self.base_interact(self.prompt)
        eval_stack = self.eval()
        eval_obj = eval_stack["LLMEval"]
        eval_obj.set_llm(self.LLM_eval_llm)
        eval_obj.set_ans(ans)
        eval_obj.set_field(self.field)
        eval_obj.set_prompt(self.prompt)
        eval_obj.set_threadnum(self.threadnum)
        LLM_eval_score, LLM_eval_info = eval_obj.score(self.methodnum[3])
        print(LLM_eval_info + f"from thread {self.threadnum}")
        score_dict["LLM_eval"] = LLM_eval_score
        final_score_obj = FinalScore1(score_dict, self.field, self.threadnum)
        human_judge, final_score_info, final_score = final_score_obj.final_score_info(self.methodnum[4])

        print(final_score_info)

        if final_score != "Human Evaluation":
            if float(final_score) <= 0.25:
                print(
                    f'Mistaken case:prompt:{self.prompt},ans:[{ans}],field:{self.field}'
                )
            if float(final_score) > 0.25:
                print(
                    f"Example case:prompt:{self.prompt},ans:[{ans}],field:{self.field}"
                )
