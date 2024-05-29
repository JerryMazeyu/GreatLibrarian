async def human_evaluation_async(human_eval, counter=[1]) -> None:
    info = ""
    for i in range(len(human_eval["prompt"])):
        info += f'\n{counter[0]}. Please score this testcase from 0-1\nThe eval_info of this testcase is:\n{human_eval["eval_info"]}'
        info += f'\nTo LLM:{human_eval["prompt"][i]}\nTo User:{human_eval["ans"][i]}\nThe final score of this testcase is "your score", in {human_eval["field"]} field.from thread {human_eval["threadnum"]}'
        counter[0] += 1
    print(info)
