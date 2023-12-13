import re
from ..Utils import add_logger, generate_logger_subfile, generate_name_new
import os
import json

temp_name = "process"
logger_subfile = generate_logger_subfile()
file_path = os.path.join("Logs", logger_subfile)
temp_path = os.path.join(file_path, f"{temp_name}.temp")


def record_process(process_info):
    if process_info is not None:
        if not os.path.exists(temp_path):
            os.makedirs(os.path.dirname(temp_path), exist_ok=True)
        with open(temp_path, "w", encoding="utf-8") as temp:
            temp.write(process_info)
