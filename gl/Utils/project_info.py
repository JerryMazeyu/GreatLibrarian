from gl.Utils.logger import generate_logger_subfile
import os
import json


# json_name = "project_info"
# if Test_ID == '':
#     logger_subfile = generate_logger_subfile()
# else:
#     logger_subfile = Test_ID
# file_path = os.path.join("Logs", logger_subfile)
# json_path = os.path.join(file_path, f"{json_name}.json")


def record_project_info(
    project_name,
    test_llm_name,
    LLM_eval_llm_name,
    testcase_path,
    testproject_num,
    Test_name,
    file_path,
) -> None:
    json_path = os.path.join(file_path, "project_info.json")
    if not os.path.exists(json_path):
        os.makedirs(os.path.dirname(json_path), exist_ok=True)

    data = {
        "project_name": project_name,
        "llm_name": test_llm_name,
        "LLM_eval_llm_name": LLM_eval_llm_name,
        "testcase_path": testcase_path,
        "testproject_num": testproject_num,
        "Test_name": Test_name,
    }

    with open(json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
