import re

def extract_example_info(log_file):

    pattern = r"Example case:prompt:\['(.*?)'\],ans:\['(.*?)'\],field:(\w+)"
    
    example_list = []

    with open(log_file,'r') as file:
        log_messages = file.readlines()

    for message in log_messages:
        match = re.search(pattern, message)
        if match:
            prompt = match.group(1)
            ans = match.group(2)
            field = match.group(3)
            example_list.append([prompt,ans,field])
    return(example_list)