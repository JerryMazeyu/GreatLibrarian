import re
from Utils import add_logger
import os

# add_logger_to_func_dialog=add_logger_name_func('dialog')
@add_logger(logger_name='dialog',logger_file='Logs')
def clean_log_dialog(log_file):
    thread_messages = info_extract(log_file)

    for i in range (1,len(thread_messages)+1):
        messages=thread_messages[str(i)]
        for message in messages:
            print(message)
        print()

def info_extract(log):
    pattern = r"from thread (\d+)"
    with open(log,'r') as file:
        log_messages = file.readlines()

    thread_messages = {}

    current_thread = None

    for message in log_messages:
        match = re.search(pattern, message)
        if match:
            current_thread = match.group(1)
            if current_thread not in thread_messages:
                thread_messages[current_thread] = []
        if current_thread:
            clean_message = re.sub(pattern, '', message).strip()
            thread_messages[current_thread].append(clean_message)
    return(thread_messages)



