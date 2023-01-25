import config
import requests
import asyncio
import aiohttp

class WordnikResult:
    defintion: str
    example: str

class WordnikClient:

    api_key = config.api_key
    wordnik_api_base_url = f"https://api.wordnik.com/v4/word.json/"
    params = {'api_key': api_key, 'limit': '1'}

    @classmethod
    async def get_word_definition(cls, word: str, session: aiohttp.ClientSession):
        url = cls.wordnik_api_base_url + f"{word}/definitions"       
        try:
            results = await cls.fetch(url,cls.params,session)
            word_def = results[0]['text']
        except:
            word_def = 'No definition found.'
        return word_def

    @classmethod
    async def get_word_example(cls, word: str, session: aiohttp.ClientSession):
        url = cls.wordnik_api_base_url + f"{word}/examples"
        try:
            results = await cls.fetch(url,cls.params,session)
            word_example = results['examples'][0]['text']
        except:
            word_example = 'No examples found.'
        return word_example

    @classmethod
    async def get_word_definition_and_example(cls, word: str) -> WordnikResult:
        async with aiohttp.ClientSession() as session:
            tasks = []
            tasks.append(asyncio.create_task(cls.get_word_definition(word,session)))
            tasks.append(asyncio.create_task(cls.get_word_example(word,session)))
            results = await asyncio.gather(*tasks)
            wordnik_result = WordnikResult()
            wordnik_result.defintion = results[0]
            wordnik_result.example = results[1]
            return wordnik_result


    @staticmethod
    async def fetch(url: str, params: dict, session: aiohttp.ClientSession):
        async with session.get(url=url,params=params) as response:
            return await response.json()

#asyncio.run(WordnikClient.get_word_definition_and_example('overhang'))