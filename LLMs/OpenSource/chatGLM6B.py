from Core import LLMs
import requests
import json
import configparser
from ..dbInteractor import get_db_connection, write_data_to_database


class ChatGLM6B(LLMs):
    def __init__(self):
        self.model = "ChatGLM-6B"
        pass

    def __call__(self, prompt: str) -> dict:  # 这里输出改成了dict
        config = configparser.ConfigParser()
        config.read('../LLMs.ini')

        api_address = config.get('chatGLM6B_Local', 'local_api_request_address')
        port = config.get('chatGLM6B_Local', 'port')

        payload = {
            "prompt": prompt,
            "history": []
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(api_address + ':' + port, headers=headers, data=payload)

        if response.status_code == 200:
            # return response.json()['response']
            data = {**payload, **response.json()}
            data['llm_name'] = self.model
            db = get_db_connection(hostname=config.get('DataBase_Settings', 'host'),
                                   username=config.get('DataBase_Settings', 'username'),
                                   password=config.get('DataBase_Settings', 'password'),
                                   dbname=config.get('DataBase_Settings', 'tablename1'))
            write_data_to_database(db=db, tablename=config.get('DataBase_Settings', 'tablename1'), data=data)
            return {**payload, **response.json()}
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
            return None


chatglm6b = ChatGLM6B()
# unit test
# response = chatglm6b.__call__("你好！")