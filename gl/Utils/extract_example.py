import re
from typing import List


def extract_example_info(log_file, test_type) -> List[List[str]]:
    pattern1 = re.compile(
        r"Example case:prompt:\s*\['(.*?)'\],\s*ans:\s*\['(.*?)'\],\s*field:\s*(.*?),\s*keywords:\s*\[(.*?)\](?:,\s*blacklist:\s*\[(.*?)\])?"
    )
    pattern2 = re.compile(
        r"Example case:prompt:\['(.*?)'\],ans:\[([^\]]+)\],field:(.*?)$"
    )

    if test_type == 'general':
        pattern = pattern1
    else:
        pattern = pattern2

    mistaken_list = []

    with open(log_file, "r", encoding="utf-8") as file:
        log_messages = file.readlines()
    if pattern == pattern1:
        for message in log_messages:
            match = re.search(pattern, message)
            if match:
                prompt = match.group(1)
                ans = match.group(2)
                field = match.group(3)
                keywords = match.group(4)
                blacklist = match.group(5)
                if blacklist is not None:
                    mistaken_list.append([prompt, ans, field, keywords, blacklist])
                else:
                    mistaken_list.append([prompt, ans, field, keywords])
    else:
        for message in log_messages:
            match = re.search(pattern, message)
            if match:
                prompt = match.group(1)
                ans = match.group(2)
                field = match.group(3)
                mistaken_list.append([prompt, ans, field])
    return mistaken_list
