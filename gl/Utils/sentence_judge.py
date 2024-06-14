from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline
from pathlib import Path

# def sentence_judge(sentence: str) -> bool:
#     local_path = Path(__file__).resolve().parent.parent / 'models' / 'sentence_judge' / 'bert-base-multilingual-uncased-sentiment'
#     tokenizer = BertTokenizer.from_pretrained(local_path)
#     model = BertForSequenceClassification.from_pretrained(local_path)
#     classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
#     results = classifier(sentence)
#     sentiment = results[0]['label']
#     if sentiment in ["1 star", "2 stars"]:
#         return False
#     else:
#         return True
    
# print(sentence_judge('" 请将以下内容翻译成英文:苹果\\n\\n\\"苹果\\"的英文翻译是\\"apple\\"'))



def sentence_judge(sentence: str) -> bool:
    negative_words = ["不", "没有", "未", "无", "别"]
    for word in negative_words:
        if word in sentence:
            return False
    return True