import re
from typing import List


def extract_mistaken_info(log_file) -> List[List[str]]:
    pattern = re.compile(
        r"Mistaken case:prompt:\s*\['(.*?)'\],\s*ans:\s*\['(.*?)'\],\s*field:\s*(.*?),\s*keywords:\s*\[(.*?)\](?:,\s*blacklist:\s*\[(.*?)\])?"
    )

    mistaken_list = []

    with open(log_file, "r", encoding="utf-8") as file:
        log_messages = file.readlines()

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
    return mistaken_list
