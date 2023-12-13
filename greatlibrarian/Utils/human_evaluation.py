import re
from ..Utils import add_logger, generate_logger_subfile, generate_name_new
import os

log_name = "human_evaluation"
logger_subfile = generate_logger_subfile()


@add_logger(log_name, os.path.join("Logs", logger_subfile))
def human_evaluation(human_eval, counter=[1]):
    info = ""
    for i in range(len(human_eval["prompt"])):
        info += f'\n{counter[0]}. Please score this testcase from 0-1\n Add rating information in the following format:\n The final score of this testcase is "your score", in {human_eval["field"]} field.from thread {human_eval["threadnum"]}'
        info += f'\nTo LLM:{human_eval["prompt"][i]}\nTo User:{human_eval["ans"][i]}'
        counter[0] += 1
    print(info)
