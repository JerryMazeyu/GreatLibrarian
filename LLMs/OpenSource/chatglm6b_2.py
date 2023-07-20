from Core import LLMs
import requests
import json
import configparser
from LLMs.dbInteractor import get_db_connection, write_data_to_database


class ChatGLM6B_2(LLMs):
    def __init__(self):
        self.model = "ChatGLM-6B-2"
        pass

    def __call__(self, prompt: str) -> str:  # 这里输出改成了dict
        config = configparser.ConfigParser()
        config.read('../LLMs.ini')

        api_address = config.get('chatGLM6B_2_Local', 'local_api_request_address')
        port = config.get('chatGLM6B_2_Local', 'port')
        req = {
            "prompt": prompt,
            "history": []
        }
        payload = json.dumps(req)
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(api_address + ':' + port, headers=headers, data=payload)
        if response.status_code == 200:
            data = {**req, **response.json()}
            data['llm_name'] = self.model
            db = get_db_connection(hostname=config.get('DataBase_Settings', 'host'),
                                   username=config.get('DataBase_Settings', 'username'),
                                   password=config.get('DataBase_Settings', 'password'),
                                   dbname=config.get('DataBase_Settings', 'tablename1'))
            write_data_to_database(db=db, tablename=config.get('DataBase_Settings', 'tablename1'), data=data)
            return {**req, **response.json()}
        else:
            # Handle request errors
            print(f"Request failed with status code {response.status_code}: {response.text}")
            return None


chatglm6b_2 = ChatGLM6B_2()
# unit test
response = chatglm6b_2.__call__("你好！请描述一下你自己。")
