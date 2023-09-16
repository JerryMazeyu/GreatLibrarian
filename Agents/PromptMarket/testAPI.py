import openai

# 使用你的API密钥初始化OpenAI API客户端
openai.api_key = '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'

# 使用Timeout属性为API调用设置超时（示例）
try:
    response = openai.Completion.create(
        engine="davinci",
        prompt="将以下英文文本翻译成法语：'Hello, how are you?'",
        max_tokens=50,
        timeout=5  # 将超时设置为5秒
    )
except openai.error.TimeoutError as e:
    print("API调用超时:", e)
except Exception as e:
    print("发生错误:", e)
