import zhipuai

zhipuai.api_key = "450fe9e4faec64c0a48234a5d92115ef.aWoqpjlhWO2Kpbvw"
 
def invoke_example():
    response = zhipuai.model_api.invoke(
        model="chatglm_pro",
        prompt=[{"role": "user", "content": "人工智能"}],
        top_p=0.7,
        temperature=0.9,
    )
    print(response)
invoke_example()