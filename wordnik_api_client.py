import requests
import config


class WordnikClient:

    def __init__(self, api_key=config.api_key):
        self.api_key = api_key

    def get_def(self, word: str) -> dict:
        url = f"https://api.wordnik.com/v4/word.json/{word}/definitions"
        params = {'api_key': self.api_key, 'limit': '1'}
        response = requests.get(url, params=params).json()
        return response
