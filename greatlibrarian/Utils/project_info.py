import re
from ..Utils import add_logger,generate_logger_subfile,generate_name_new
import os
import json

json_name = 'project_info'
logger_subfile = generate_logger_subfile()
file_path = os.path.join('Logs',logger_subfile)
json_path = os.path.join(file_path, f'{json_name}.json')

def record_project_info(project_name,test_llm_name,GPT4_eval_llm_name,testcase_path,testproject_num):
    if not os.path.exists(json_path):
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

    # 创建一个包含指定内容的字典
    data = {'project_name':project_name,'llm_name':test_llm_name,'GPT4_eval_llm_name':GPT4_eval_llm_name,'testcase_path':testcase_path,'testproject_num':testproject_num}

    # 将字典内容写入 JSON 文件
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)