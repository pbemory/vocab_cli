import requests
import json
import config


class WordnikClient:

    api_key = config.api_key

    @classmethod
    def get_word_definition(cls, word: str) -> str:
        url = f"https://api.wordnik.com/v4/word.json/{word}/definitions"
        params = {'api_key': cls.api_key, 'limit': '1'}
        response = requests.get(url, params=params).json()
        word_def = response[0]['text']
        return word_def

    @classmethod
    def get_word_example(cls, word:str) -> str:
        url = f"https://api.wordnik.com/v4/word.json/{word}/examples"
        params = {'api_key': cls.api_key, 'limit': '1'}
        response = requests.get(url,params=params).json()
        word_example = response['examples'][0]['text']
        return word_example

