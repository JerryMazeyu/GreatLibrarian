import json
import re
import itertools
from copy import deepcopy
from collections import defaultdict
from Utils import to_list
from warnings import warn


class TestProject:
    def __init__(self, json_obj):
        self.name = json_obj.get('name', "No Test Case Name")
        self.description = json_obj.get('description', "")
        self.fields = []
        self.prompts_ = json_obj['prompts']
        self.values = json_obj.get('values', {})
        self.raw_eval_info = json_obj.get('evaluation', None)
        self.valid_fields = ['common knowledge', 'tool usage']
        self.prompts = defaultdict(list)

        if isinstance(json_obj['field'], list):
            for x in json_obj['field']:
                if x not in self.valid_fields:
                    print(f"Warning: Field '{x}' is not in {self.valid_fields}")
                else:
                    self.fields.append(x)
        else:
            if json_obj['field'] not in self.valid_fields:
                print(f"Warning: Field '{json_obj['field']}' is not in {self.valid_fields}")
            else:    
                self.fields.append(json_obj['field'])
        
        self.get_prompts()
        self.get_eval_info()
        
    def get_value_list(self, valuestr:str):
        """From template to value list.

        Args:
            valuestr (str): Value string like ${1} ${2.1}

        Returns:
            list: Value list.
        """
        result = []
        value = re.findall(r'{\$((?:\d+\.\d+)|(?:\d+))}', valuestr)
        assert len(value) == 1, ValueError("Wrong template.")
        value = value[0].split('.')
        return self.values[value[0]]
        
    
    def replace_placeholders(self, template, ind_):
        """Replace placeholder into template prompt

        Args:
            template (Union[str, list]): prompt string or list
        """
        tmplstr = template if isinstance(template, str) else ' '.join(template)
        placeholders = re.findall(r'\{\$.*?\}', tmplstr)
        
        inds = list(set([list(map(int, re.findall(r'{\$((?:\d+\.\d+)|(?:\d+))}', p)[0].split('.')[0]))[0] for p in placeholders]))

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
                tmp = re.findall(r'{\$((?:\d+\.\d+)|(?:\d+))}', p)[0].split('.')
                if len(tmp) == 1:
                    rep_dict[p] = rp[int(tmp[0])]
                else:
                    rep_dict[p] = rp[int(tmp[0])][int(tmp[1])-1]
            
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
            
    def get_prompts(self):
        """Get all prompts
        """
        for ind, p in enumerate(self.prompts_):
            self.replace_placeholders(p, ind)
    
    def get_eval_info(self):
        for key, pt in self.prompts.items():
            assert(len(self.prompts[key]) == len(self.raw_eval_info[str(key)])), ValueError(f"[{key}] Test promopt length {len(self.prompts[key])} don't match the evaluation info {len(self.raw_eval_info[str(key)])}")
            # print(self.raw_eval_info[str(key)])
    
    def get_cases(self, baseconf=None):
        """The main function of the TestProject

        Yields:
            dict: Return a iterable dict which contains a case.
        """ 
        for k,v in self.prompts.items():
            for ind, pr in enumerate(v):
                cfg = {'name': self.name, 'description': self.description, 'field':to_list(self.fields), \
                        'prompt': to_list(pr), 'eval_info': self.raw_eval_info[str(k)][ind]}
                if baseconf:
                    cfg['llm'] = getattr(baseconf, 'llm', None)
                    cfg['register_agents'] = getattr(baseconf, 'register_agents', None)
                    if not cfg['register_agents']:
                        warn("There is no registered agents in the config.", RuntimeWarning)
                yield cfg
                




# jsonstr = """
# {
# "name": "example1",
# "description": "Test if LLM can recognize common knowledge.",
# "field": "common knowledge",
# "promots": [
#     "{$1.1} is {$1.2}, do you think this is right?",
#     ["What do you think about {$2.1} and {$2.2}?", "You are wrong, rethink this."],
#     "{$3} is a city from {$4}, yes or no?"
# ],
# "values": {
#     "1": [["鲁迅", "周树人"], ["李白", "诗圣"]],
#     "2": [["Pi", "3.14"], ["上海", "魔都"]],
#     "3": ["New York", "London", "Beijing"],
#     "4": ["China"]
# },
# "evaluation": {
#     "0": [{"keywords":["yes", "same"], "GPT4eval": true}, {"keywords":["no", "different", "杜甫"], "GPT4eval": true}],
#     "1": [{"keywords":["yes", "larger", "bigger"]}, {"keywords":["yes"], "balcklist": ["no"]}],
#     "2": [{"keywords":["yes"]}, {"keywords":["no"]}, {"keywords":["no"]}]
# }
# }
# """
# jsobj = json.loads(jsonstr)
# tp = TestProject(jsobj)
# tp.get_prompts()
# for i in tp.get_cases():
#     print(i)