from Core import LLMs
import requests
import json
import configparser


class ChatGLM6B(LLMs):
    def __init__(self):
        self.model = "ChatGLM-6B"
        pass

    def __call__(self, prompt: str) -> str:
        # Read the INI file and extract the API address
        config = configparser.ConfigParser()
        config.read('../LLMs.ini')  # Replace 'your_ini_file.ini' with the actual file path

        api_address = config.get('chatGLM6B_Local', 'local_api_request_address')

        # Prepare the JSON payload
        payload = {
            "prompt": prompt,
            "history": []
        }
        headers = {
            'Content-Type': 'application/json'
        }
        # Make the HTTP POST request with the JSON payload
        response = requests.post(api_address, headers=headers, data=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.json()['response']
        else:
            # Handle request errors
            print(f"Request failed with status code {response.status_code}: {response.text}")
            return None


chatglm6b = ChatGLM6B()
# unit test
# response = chatglm6b.__call__("你好！")
