import requests
import dotenv
import os
import json

class OpenApiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://api.openai.com/v1/chat/completions'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_word_definition(self, word):
        prompt = f"Provide the definition and couple of examples of the word '{word}'. Response in json."

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 250
        }

        response = requests.post(self.api_url, headers=self.headers, json=data)
        response_json = response.json()

        if response.status_code == 200:
            content = json.loads(response_json['choices'][0]['message']['content'])
            return content["definition"], content["examples"], 200
        else:
            return response.json(), None, response.status_code

class Ai:
    def __init__(self):
        self.init_env()
        self.client = OpenApiClient(self.api_key)
        
    def init_env(self):
        env_path = './.env'
        if not os.path.exists(env_path):
            env_path = os.path.expanduser('~/.telesm.conf')
            if not os.path.exists(env_path):
                raise Exception("No API Key could be found.")
        
        dotenv.load_dotenv(env_path)
        api_key = os.getenv("OPENAPI_API_KEY")
        if not api_key:
            raise Exception(f"Please specify your api key in {env_path}")
        self.api_key = api_key
        
    def get_definition(self, word):
        return self.client.get_word_definition(word)