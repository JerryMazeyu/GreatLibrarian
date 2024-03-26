import re
from typing import Dict, List


def clean_log_dialog(log_file) -> None:
    """Organize disordered logs in the order of line numbers to create properly ordered logs."""
    thread_messages = info_extract(log_file)

    for i in range(1, len(thread_messages) + 1):
        messages = thread_messages[str(i)]
        for message in messages:
            # Check if the message contains the specified patterns
            if (
                "Mistaken case:prompt:" not in message
                and "Example case:prompt:" not in message
            ):
                print(message)
        print()


def info_extract(log) -> Dict[str, List[str]]:
    pattern = r"from thread (\d+)"
    with open(log, "r", encoding="utf-8") as file:
        log_messages = file.readlines()

    thread_messages = {}
    current_thread = None
    multi_line_message = ""

    for message in log_messages:
        match = re.search(pattern, message)
        if match:
            current_thread = match.group(1)
            if current_thread not in thread_messages:
                thread_messages[current_thread] = []

            if multi_line_message:
                thread_messages[current_thread].append(multi_line_message.strip())
                multi_line_message = ""

        if current_thread:
            if current_thread and not match:
                multi_line_message += message
            else:
                clean_message = re.sub(pattern, "", message).strip()
                thread_messages[current_thread].append(clean_message)

    return thread_messages
