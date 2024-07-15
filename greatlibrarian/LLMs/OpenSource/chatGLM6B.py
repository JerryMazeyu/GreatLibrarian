from greatlibrarian.Core import LLMs
import requests
import json
import configparser
from greatlibrarian.LLMs.dbInteractor import get_db_connection, write_data_to_database


class ChatGLM6B(LLMs):
    def __init__(self):
        self.model = "ChatGLM-6B"
        pass

    def __call__(self, prompt: str) -> dict:  # 这里输出改成了dict
        config = configparser.ConfigParser()
        config.read("../LLMs.ini")

        api_address = config.get("chatGLM6B_1_Local", "local_api_request_address")
        port = config.get("chatGLM6B_1_Local", "service_port")

        payload = {"prompt": prompt, "history": []}
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            api_address + ":" + port, headers=headers, data=json.dumps(payload)
        )

        if response.status_code == 200:
            data = {**payload, **response.json()}
            data["llm_name"] = self.model
            db = get_db_connection(
                hostname=config.get("chatGLM6B_1_Local", "host"),
                port=int(config.get("chatGLM6B_1_Local", "db_port")),
                username=config.get("chatGLM6B_1_Local", "username"),
                password=config.get("chatGLM6B_1_Local", "password"),
                dbname=config.get("chatGLM6B_1_Local", "database"),
            )
            write_data_to_database(
                db=db, tablename=config.get("chatGLM6B_1_Local", "tablename"), data=data
            )
            return {**payload, **response.json()}
        else:
            print(
                f"Request failed with status code {response.status_code}: {response.text}"
            )
            return None


chatglm6b = ChatGLM6B()
# unit test
# response = chatglm6b.__call__("你好！")
