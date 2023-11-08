import re
from Utils import add_logger,generate_logger_subfile,generate_name_new
import os

# log_name = generate_name_new('dialog')
log_name = 'dialog'
logger_subfile = generate_logger_subfile()

@add_logger(log_name,os.path.join('Logs',logger_subfile))
def clean_log_dialog(log_file):
    """
    Organize disordered logs in the order of line numbers to create properly ordered logs.

    """
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



