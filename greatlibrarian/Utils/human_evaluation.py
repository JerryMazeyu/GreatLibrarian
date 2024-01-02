from ..Utils import add_logger, generate_logger_subfile

# log_name = "human_evaluation"
# if Test_ID == '':
#     logger_subfile = generate_logger_subfile()
# else:
#     logger_subfile = Test_ID


# @add_logger(log_name, os.path.join("Logs", logger_subfile))
def human_evaluation(human_eval, counter=[1]) -> None:
    info = ""
    for i in range(len(human_eval["prompt"])):
        info += f'\n{counter[0]}. Please score this testcase from 0-1\n Add rating information in the following format:\nThe final score of this testcase is "your score", in {human_eval["field"]} field.from thread {human_eval["threadnum"]}'
        info += f'\nTo LLM:{human_eval["prompt"][i]}\nTo User:{human_eval["ans"][i]}'
        counter[0] += 1
    print(info)
