from testregist import wx


llm_cfg = dict(type='qwen_turbo',apikey = 'test', name = 'name')
print(llm_cfg)

def test(type,apikey=1,name=2):
    print(type,apikey,name)

test(**llm_cfg)