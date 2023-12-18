from ...Core import LLMs
import zhipuai

import dashscope

import qianfan


class chatglm_pro(LLMs):
    """A LLM used in GreatLibrarian:chatglm_pro"""

    def __init__(self) -> None:
        self.apikey = "450fe9e4faec64c0a48234a5d92115ef.aWoqpjlhWO2Kpbvw"
        self.name = "chatglm_pro"
        self.llm_intro = "ChatGLMpro 是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。\n\nChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。\n\n相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n1.高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n2.丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n3.强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n4.个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n5.开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。\n\n"

    def __call__(self, prompt: str) -> str:
        zhipuai.api_key = self.apikey
        response = zhipuai.model_api.invoke(
            model="chatglm_pro",
            prompt=[{"role": "user", "content": prompt}],
            top_p=0.7,
            temperature=0.9,
        )
        if response["code"] == 200:
            return response["data"]["choices"][0]["content"]
        else:
            return "API Problem"


class qwen_turbo(LLMs):
    """A LLM used in GreatLibrarian:qwen_turbo"""

    def __init__(self) -> None:
        self.apikey = "sk-9ca2ad73e7d34bd4903eedd6fc70d0d8"
        self.name = "qwen_turbo"
        self.llm_intro = "通义千问是由阿里巴巴集团开发的一款人工智能语言模型应用，它采用了大规模机器学习技术，能够模拟人类自然语言的能力，提供多种服务，如文本翻译、聊天机器人、\n\n自动回复、文档摘要等。\n\n它的核心特点是多轮对话，可以理解用户的意图并进行有效的回复；同时，它还具有强大的文案创作能力，可以为用户提供优秀的文字创意，比如续写小说、撰写邮件等。\n\n此外，通义千问还具备多模态的知识理解能力，可以识别图片、音频、视频等多种媒体形式，并从中提取出关键信息。不仅如此，通义千问还支持多语言，可以实现中文、\n\n英文等不同语言之间的自由转换。\n\n目前，通义千问正在接受内测阶段，并已在各大手机应用市场上线，所有人都可以通过APP直接体验最新模型能力。\n\n"

    def __call__(self, prompt: str) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
            model=dashscope.Generation.Models.qwen_turbo, prompt=prompt
        )

        if response:
            if response["output"]:
                if response["output"]["text"]:
                    return response["output"]["text"]
        return "API Problem"


class wenxin(LLMs):
    """A LLM used in GreatLibrarian:wenxin"""

    def __init__(self) -> None:
        self.ak = "B00yKgZuin8IolPHYsHggVyU"
        self.sk = "B19OtdVn0jwwaByK9RgovfukUQWv2rT6"
        self.name = "wenxin"
        self.llm_intro = "百度是一家全球领先的人工智能公司，拥有强大的技术实力和丰富的数据资源。近年来，百度在自然语言处理领域取得了重大突破，其中最具代表性的就是文心一言。技术原理：文心一言是基于深度学习算法和大规模语料库训练得到的。它采用了Transformer架构，这是一种基于自注意力机制的神经网络结构。通过多轮训练和优化，文心一言可以学会从海量文本中提取语义信息，并根据上下文生成合理的回复。\n\n功能特点：\n\n（1）对话互动：文心一言能够与用户进行自然对话，理解并回答用户的问题，提供相关的知识和信息。\n\n（2）回答问题：文心一言可以针对用户提出的问题进行快速回答，无需等待人工响应。\n\n（3）协助创作：文心一言能够根据用户的创作需求，提供灵感和素材，帮助用户更好地完成写作任务。\n\n（4）多语言支持：文心一言支持多种语言，可以为不同语言的用户提供服务。\n\n（5）知识推理：文心一言具备进行知识推理的能力，可以根据已有的知识进行推理，为用户提供更为精准的信息。\n\n应用场景：\n\n（1）搜索引擎：百度将文心一言应用于搜索引擎中，为用户提供更为准确和及时的搜索结果。\n\n（2）智能客服：文心一言可以应用于企业客服系统中，提高客户服务效率和质量。\n\n（3）智能家居：文心一言可以与智能家居设备结合，为用户提供更为智能化的家居生活体验。\n\n（4）教育领域：文心一言可以为教育领域提供支持，辅助教师进行教学和学生进行自主学习。\n\n（5）其他领域：文心一言还可以应用于新闻媒体、广告营销、金融投资等领域，提高工作效率和服务质量。\n\n未来发展：\n\n随着技术的不断进步和应用场景的不断扩展，文心一言将会拥有更加广泛的应用前景。百度将继续投入大量资源和精力，对文心一言进行持续优化和升级，提高其性能和智能化\n\n程度，为用户提供更为优质的服务。同时，百度也将加强与各行业企业的合作，推动人工智能技术的普及和应用，促进社会进步和发展。\n\n"

    def __call__(self, prompt: str) -> str:
        # 替换下列示例中参数，应用API Key替换your_ak，Secret Key替换your_sk
        chat_comp = qianfan.ChatCompletion(ak=self.ak, sk=self.sk)

        # 指定特定模型
        resp = chat_comp.do(
            model="ERNIE-Bot", messages=[{"role": "user", "content": prompt}]
        )

        if resp:
            if resp["body"]:
                if resp["body"]["result"]:
                    return resp["body"]["result"]
        return "API Problem"
