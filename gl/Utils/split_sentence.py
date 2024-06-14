import re 
from typing import List

# def split_sentences(text: str) -> List[str]:
#     # 使用正则表达式在句号、问号、感叹号和分号之后分割句子
#     sentences = re.split(r'[。？！；——，.?!;,]', text)
#     # 去除空白句子
#     sentences = [sent.strip() for sent in sentences if sent.strip()]
#     return sentences

# print(split_sentences(" 我国位置最北、纬度最高的省级行政区是黑龙江省。"))

def split_response(text: str) -> List[str]:
    # 使用正则表达式在句号、问号、感叹号和分号之后分割句子
    sentences = re.split(r'[。？！；——，.?!;,]', text)
    # 去除空白句子
    sentences = [sent.strip() for sent in sentences if sent.strip()]
    return sentences