import openai

# 使用你的API密钥初始化OpenAI API客户端


try:
    response = openai.Completion.create(
        engine="davinci",
        prompt="将以下英文文本翻译成法语：'Hello, how are you?'",
        max_tokens=50,
        timeout=5  # 将超时设置为5秒
    )
except openai.error.OpenAIError as e:
    print("API调用错误:", e)
except Exception as e:
    print("发生错误:", e)
