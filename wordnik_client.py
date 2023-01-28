import config
import asyncio
import aiohttp

class WordnikResult:

    def __init__(self, definition: str, example: str):
        self.definition = definition
        self.example = example

class WordnikClient:

    api_key = config.api_key
    wordnik_api_base_url = f"https://api.wordnik.com/v4/word.json/"
    params = {'api_key': api_key, 'limit': '1'}

    async def get_word_definition(self, word: str, session: aiohttp.ClientSession):
        url = self.wordnik_api_base_url + f"{word}/definitions"       
        try:
            results = await self.fetch(url,self.params,session)
            word_def = results[0]['text']
        except Exception as e:
            word_def = 'No definition found.'
        return word_def

    async def get_word_example(self, word: str, session: aiohttp.ClientSession):
        url = self.wordnik_api_base_url + f"{word}/examples"
        try:
            results = await self.fetch(url,self.params,session)
            word_example = results['examples'][0]['text']
        except Exception as e:
            word_example = 'No examples found.'
        return word_example

    async def get_word_definition_and_example(self, word: str) -> WordnikResult:
        async with aiohttp.ClientSession() as session:
            tasks = []
            tasks.append(asyncio.create_task(self.get_word_definition(word,session)))
            tasks.append(asyncio.create_task(self.get_word_example(word,session)))
            results = await asyncio.gather(*tasks)
            wordnik_result = WordnikResult(definition=results[0],example=results[1])
            return wordnik_result


    async def fetch(self, url: str, params: dict, session: aiohttp.ClientSession):
        async with session.get(url=url,params=params) as response:
            return await response.json()

'''
Code below for debugging.
'''
# wordnik_result = asyncio.run(WordnikClient.get_word_definition_and_example('parsimony'))
# print(wordnik_result.definition)
# print(wordnik_result.example)