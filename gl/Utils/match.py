from sentence_transformers import SentenceTransformer, util
from pathlib import Path
import math

# def get_match(input: str, keyword: str) -> bool:
#     model_path = Path(__file__).resolve().parent.parent / 'models' / 'match' / 'S-bert'
#     model = SentenceTransformer(str(model_path))
#     # model = SentenceTransformer(model_path)
#     embedding_str = model.encode(input, convert_to_tensor=True)
#     embedding_keyword = model.encode(keyword, convert_to_tensor=True)
#     cosine_sim = util.pytorch_cos_sim(embedding_str, embedding_keyword)
#     if cosine_sim > 0.50 :
#         print(f'{input}和{keyword}匹配，相似度为：{cosine_sim}')
#         return True
#     else: 
#         print(f'{input}和{keyword}不匹配，相似度为：{cosine_sim}')
#         return False


# get_match('小明是我们学校最优秀的老师','小明不是我们学校最优秀的老师')
# get_match('西红柿','番茄')

def get_sim(sen1: str, sen2: str, model) -> list:
    """
    Match method supported by BGE3.
    sen1 is the sentence split from the response from LLM.
    sen2 is one of the keywords from the testcase.
    model is used to calculate the similarity between sen1 and sen2.
    """
    model = model
    kl = len(sen2)
    new_str_list = split_sen(sen1, kl)
    print(new_str_list)
    embeddings_1 = model.encode(new_str_list, 
                                batch_size=12, 
                                max_length=256,)['dense_vecs']
    embeddings_2 = model.encode(sen2)['dense_vecs']
    similarity = embeddings_1 @ embeddings_2.T
    max_sim = max(similarity)
    return max_sim


def split_sen(sen: str, keyword_len: int) -> list:
    sl = len(sen)
    kl = keyword_len
    split_result = []
    if sl > kl:
        kl_left = kl - kl/2
        left = math.ceil(kl_left)
        window_left = max(1, left)
        kl_right = kl + kl/2
        right = math.ceil(kl_right)
        window_right = min(sl, right)
        split_result = []
        for i in range(window_left, window_right+1):
            split_result = extract_substrings(sen, i, split_result)
        return split_result
    else:
        split_result.append(sen)
        return split_result
    

def extract_substrings(input_string, l, str_list):
    new_str_list = str_list
    i = 0
    while i <= len(input_string) - l:
        substring = input_string[i:i+l]
        new_str_list.append(substring)
        i += 1
    return new_str_list


# response = "今天天气不错阳光很好没有下雨"
# keywords = "晴天"
# kl = len(keywords)
# print(split_sen(response,kl))

# from FlagEmbedding import BGEM3FlagModel
# def get_model():
#     model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
#     return model
# model = get_model()

# print(get_sim(response, keywords, model))