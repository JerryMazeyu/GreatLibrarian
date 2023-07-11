import json
import re
import itertools
from copy import deepcopy


class TestProject:
    def __init__(self, json_obj):
        self.name = json_obj.get('name', "No Test Case Name")
        self.description = json_obj.get('description', "")
        self.fields = []
        self.prompts_ = json_obj['promots']
        self.values = json_obj.get('values', {})
        self.evaluation = json_obj.get('evaluation', None)
        self.valid_fields = ['common knowledge', 'tool usage']
        self.prompts = []

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
        
    
    def replace_placeholders(self, template):
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
            self.prompts.append(tmpl)
            
    
    def get_prompts(self):
        """Get all prompts
        """
        for p in self.prompts_:
            self.replace_placeholders(p)
        
            

