import re
import itertools
from copy import deepcopy
from collections import defaultdict
from gl.Utils import to_list
from warnings import warn
from typing import Generator, Dict, List, Any


class TestProject:
    """A class to extract test cases from test projects"""

    def __init__(self, json_obj) -> None:
        self.name = json_obj.get("name", "No Test Case Name")
        self.description = json_obj.get("description", "")
        self.fields = json_obj.get("field")
        self.prompts_ = to_list(json_obj["prompts"])
        self.values = json_obj.get("values", {})
        self.raw_eval_info = json_obj.get("evaluation", None)
        self.prompts = defaultdict(list)

        self.get_prompts()
        self.get_eval_info()

    def get_value_list(self, valuestr: str) -> List[int]:
        """
        From template to value list.

        Args:
            valuestr (str): Value string like ${1} ${2.1}

        Returns:
            list: Value list.
        """
        value = re.findall(r"{\$((?:\d+\.\d+)|(?:\d+))}", valuestr)
        assert len(value) == 1, ValueError("Wrong template.")
        value = value[0].split(".")
        return self.values[value[0]]

    def replace_placeholders(self, template, ind_) -> None:
        """
        Replace placeholder into template prompt

        Args:
            template (Union[str, list]): prompt string or list
        """
        tmplstr = template if isinstance(template, str) else " ".join(template)
        placeholders = re.findall(r"\{\$.*?\}", tmplstr)

        inds = list(
            set(
                [
                    list(
                        map(
                            int,
                            re.findall(r"{\$((?:\d+\.\d+)|(?:\d+))}", p)[0].split(".")[
                                0
                            ],
                        )
                    )[0]
                    for p in placeholders
                ]
            )
        )

        replacements = []
        for ind in inds:
            valuestr = f"{{${ind}}}"
            values = self.get_value_list(valuestr)
            replacements.append(values)
        replacements = list(itertools.product(*replacements))
        replacements_dict = [dict(zip(inds, rp)) for rp in replacements]

        rep_dict = {}
        for rp in replacements_dict:
            for p in placeholders:
                tmp = re.findall(r"{\$((?:\d+\.\d+)|(?:\d+))}", p)[0].split(".")
                if len(tmp) == 1:
                    rep_dict[p] = rp[int(tmp[0])]
                else:
                    rep_dict[p] = rp[int(tmp[0])][int(tmp[1]) - 1]

            tmpl = deepcopy(template)

            if isinstance(tmpl, list):
                for ind, pt_ in enumerate(tmpl):
                    for k, v in rep_dict.items():
                        pt_ = pt_.replace(k, v)
                    tmpl[ind] = pt_

            else:
                for k, v in rep_dict.items():
                    tmpl = tmpl.replace(k, v)
            self.prompts[ind_].append(tmpl)

    def get_prompts(self) -> None:
        """
        Get all prompts
        """
        for ind, p in enumerate(self.prompts_):
            self.replace_placeholders(p, ind)

    def get_eval_info(self) -> None:
        for key, pt in self.prompts.items():
            print(self.raw_eval_info[str(key)])
            assert len(self.prompts[key]) == len(
                self.raw_eval_info[str(key)]
            ), ValueError(
                f"[{key}] Test promopt length {len(self.prompts[key])} don't match the evaluation info {len(self.raw_eval_info[str(key)])}"
            )
            print(self.raw_eval_info[str(key)])

    def get_cases(self, baseconf=None) -> Generator[Dict[str, Any], None, None]:
        """
        The main function of the TestProject

        Yields:
            dict: Return a iterable dict which contains a case.
        """
        for k, v in self.prompts.items():
            for ind, pr in enumerate(v):
                cfg = {
                    "name": self.name,
                    "description": self.description,
                    "field": self.fields,
                    "prompt": to_list(pr),
                    "eval_info": self.raw_eval_info[str(k)][ind],
                }
                if baseconf:
                    cfg["test_llm"] = getattr(baseconf, "test_llm", None)
                    cfg["LLM_eval_llm"] = getattr(baseconf, "LLM_eval_llm", None)
                    cfg["register_agents"] = getattr(baseconf, "register_agents", None)
                    if not cfg["register_agents"]:
                        warn(
                            "There is no registered agents in the config.",
                            RuntimeWarning,
                        )
                yield cfg
