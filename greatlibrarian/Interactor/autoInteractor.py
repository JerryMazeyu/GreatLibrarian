from ..Utils import (
    load_from_cfg,
    human_evaluation,
    setup,
    apply_decorator_to_func,
)
from ..EvalMethods import ToolUse, Keyword, LLMEval, Blacklist
import warnings


class AutoInteractor:
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
        ans_list = []
        for ind, pr in enumerate(prompt):
            # recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr} from thread {self.threadnum}")
            # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.test_llm(pr)
            # ans = "Yes"
            print(f"To User:\t {ans} from thread {self.threadnum}")

            try:
                ans_list.append(ans.lower())
            except Exception as e:
                warning_message = f"Warning: An API exception occurred - {e}"
                warnings.warn(warning_message, RuntimeWarning)
                ans_list.append("default_value")

        return ans_list

    # def base_interact(self, prompt) -> list:
    #     """
    #     A function to create the interaction between the LLM and the user.
    #     It will record the dialogue in the log file and the answers to prompts sent to LLM from the LLM will be saved in a list called ans_list.
    #     In this method, the dialogue mainly contains the propmts that the user sends to LLM, and the response from the LLM.
    #     """
    #     # recoder = Recoder()
    #     # recoder.ind = ind
    #     print(f"---------- New Epoch ---------- from thread {self.threadnum}")
    #     ans_list = []
    #     for ind, pr in enumerate(prompt):
    #         # recoder.dialoge[ind] = ''
    #         i = 0
    #         history = []
    #         while i < 3:

    #             print(f"To LLM:\t {pr} from thread {self.threadnum}")
    #             # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
    #             ans = self.test_llm(pr,history)
    #             print(history)
    #             dict = {'user': pr,
    #                 'bot': ans}
    #             history.append(dict)
    #             # ans = "Yes"
    #             print(f"To User:\t {ans} from thread {self.threadnum}")
    #             i += 1

    #             try:
    #                 ans_list.append(ans.lower())
    #             except Exception as e:
    #                 warning_message = f"Warning: An API exception occurred - {e}"
    #                 warnings.warn(warning_message, RuntimeWarning)
    #                 ans_list.append("default_value")

    #     return ans_list

    # recoder.dialoge[ind] += f"To User:\t {ans}"
    # self.recoders.append(recoder)

    def tool_interact(self, prompt, tools: list) -> list:
        """
        A function to create the interaction between the LLM, the user and the tool.
        It will record the dialogue in the log file and the content that LLM sends to the tool will be saved in a list called ans_list.
        In this method, the dialogue mainly contains the propmts that the user sends to LLM, the content that the LLM sends to the tool and the response from the tool.
        """
        # recoder = Recoder()
        # recoder.ind = ind
        # recoder.prompt = prompt
        print(f"---------- New Epoch ---------- from thread {self.threadnum}")
        ans_list = []
        for ind, pr in enumerate(prompt):
            # recoder.dialoge[ind] = ''
            print(f"To LLM:\t {pr} from thread {self.threadnum}")
            # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
            ans = self.test_llm(pr)
            ans_list.append(ans.lower())
            if ans.find(tools[0]["name"]) != -1:  # TODO: add multi tools
                # recoder.tools = tools[0].name
                print(f"To Tool:\t {ans} from thread {self.threadnum}")
                # recoder.dialoge[ind] += f"To LLM:\t {pr}\n"
                tool_response = self.tools[0](ans)
                print(f"To LLM:\t {tool_response} from thread {self.threadnum}")
                # recoder.dialoge[ind] += f"To LLM:\t {tool_response}\n"
                ans = self.llm(tool_response)
            print(f"To User:\t {ans} from thread {self.threadnum}")
        #     recoder.dialoge[ind] += f"To LLM:\t {tool_response}\n"
        # self.recoders.append(recoder)
        return ans_list

    def run(self) -> None:
        """
        A function to start the interaction.
        If the interaction contains tools, it will record the dialogue between the tool, the user and the LLM.
        If the interaction doesn't contain tools, it will record the dialogue between the user and the LLM.
        The function use a list to record the answers from the LLM, and use this answer list to evaluate the LLM in this testcase. It will evaluate the LLM with every method chosen by the user.
        """
        eval_stack = self.eval()
        blacklist_score = 1
        score_dict = {}
        if self.eval_info.get("tool", None):
            toolusage_ans = self.tool_interact(self.prompt, self.eval_info["tool"])
            eval_obj = eval_stack["tool"]
            eval_obj.set_ans(toolusage_ans)
            eval_obj.set_field(self.field)
            eval_obj.set_threadnum(self.threadnum)
            toolusage_score, tool_eval_info = eval_obj.score(self.methodnum[0])
            print(tool_eval_info + f"from thread {self.threadnum}")
            score_dict["toolusage"] = toolusage_score
        else:
            keywords_ans = self.base_interact(self.prompt)
            if self.eval_info.get("blacklist", None):
                eval_obj = eval_stack["blacklist"]
                eval_obj.set_ans(keywords_ans)
                eval_obj.set_field(self.field)
                eval_obj.set_threadnum(self.threadnum)
                blacklist_score, blacklist_eval_info = eval_obj.score(self.methodnum[2])
                print(blacklist_eval_info + f"from thread {self.threadnum}")
                score_dict["blacklist"] = blacklist_score

            if blacklist_score != 0 and self.eval_info.get("keywords", None):
                eval_obj = eval_stack["keywords"]
                eval_obj.set_ans(keywords_ans)
                eval_obj.set_field(self.field)
                eval_obj.set_threadnum(self.threadnum)
                keywords_score, keywords_eval_info = eval_obj.score(self.methodnum[1])
                print(keywords_eval_info + f"from thread {self.threadnum}")
                score_dict["keywords"] = keywords_score

            if blacklist_score != 0 and self.eval_info.get("LLMEval", None):
                eval_obj = eval_stack["LLMEval"]
                eval_obj.set_llm(self.LLM_eval_llm)
                eval_obj.set_ans(keywords_ans)
                eval_obj.set_field(self.field)
                eval_obj.set_prompt(self.prompt)
                eval_obj.set_threadnum(self.threadnum)
                LLM_eval_score, LLM_eval_info = eval_obj.score(self.methodnum[3])
                print(LLM_eval_info + f"from thread {self.threadnum}")
                score_dict["LLM_eval"] = LLM_eval_score
        final_score_obj = self.finalscore(score_dict, self.field, self.threadnum)
        human_judge, final_score_info, final_score = final_score_obj.final_score_info()

        if human_judge != "Human Evaluation":
            print(final_score_info)
        else:
            print("Human Evaluation!" + f"from thread {self.threadnum}")
            human_eval = {
                "prompt": self.prompt,
                "ans": keywords_ans,
                "field": self.field,
                "threadnum": self.threadnum,
                "eval_info": self.eval_info,
            }
            dec = setup(logger_name="human_evaluation", logger_file=self.logger_path)
            self.human_evaluation = apply_decorator_to_func(
                dec(), self.human_evaluation
            )
            self.human_evaluation(human_eval)
        if final_score != 'Human Evaluation':
            if float(final_score) <= 0.5:
                if "blacklist" in self.eval_info:
                    print(
                        f'Mistaken case:prompt:{self.prompt},ans:{keywords_ans},field:{self.field},keywords:{self.eval_info["keywords"][0]},blacklist:{self.eval_info["blacklist"][0]}'
                    )
                else:
                    print(
                        f'Mistaken case:prompt:{self.prompt},ans:{keywords_ans},field:{self.field},keywords:{self.eval_info["keywords"][0]}'
                    )

            if float(final_score) > 0.5 and final_score != "Human Evaluation":
                print(
                    f"Example case:prompt:{self.prompt},ans:{keywords_ans},field:{self.field}"
                )

