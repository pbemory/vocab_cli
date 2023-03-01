import asyncio
import aiohttp
import config


class WordResult:
    """Used for storing results of fetches from dictionary apis into consumable object."""

    def __init__(self, definition: str, example: str):
        self.definition = definition
        self.example = example


class WordClient:
    """Client for interacting with WordsAPI and Wordnik API."""

    words_api_headers = config.words_api_headers
    words_api_base_url = "https://wordsapiv1.p.rapidapi.com/words/"
    wordnik_api_base_url = "https://api.wordnik.com/v4/word.json/"
    wordnik_params = {'api_key': config.wordnik_api_key, 'limit': '3'}

    async def get_words_api_definition(self, word: str, session: aiohttp.ClientSession) -> str:
        """Fetch definition of provided word from WordsAPI."""
        url = self.words_api_base_url + f"{word}/definitions"
        word_def = "No definition found."
        try:
            definitions_response = await self.fetch(url, self.words_api_headers, session)
            error_key = 'message'
            if error_key in definitions_response:
                word_def = "Error: " + definitions_response[error_key]
            else:
                definitions = definitions_response.get('definitions')
                if len(definitions) > 0:
                    word_def = definitions[0]['definition']
        except Exception as exc:
            word_def = "Exception: " + str(exc)
        return word_def

    async def get_words_api_example(self, word: str, session: aiohttp.ClientSession) -> str:
        """Fetch example of provided word from WordsAPI."""
        url = self.words_api_base_url + f"{word}/examples"
        word_example = "No example found."
        try:
            examples_response = await self.fetch(url, self.words_api_headers, session)
            examples = examples_response.get('examples')
            if len(examples) > 0:
                word_example = examples[0]
        except Exception as exc:
            word_example = "Exception: " + str(exc)
        return word_example

    async def get_wordnik_api_example(self, word: str, session: aiohttp.ClientSession) -> str:
        """Fetch example of provided word. Try 3 of wordnik's sources (using wordnik_params)."""
        url = self.wordnik_api_base_url + f"{word}/examples"
        word_example = "No example found."
        try:
            examples = await self.fetch(url, self.wordnik_params, session)
            example_key = 'text'
            error_key = 'message'
            if error_key in examples:
                word_example = "Error: " + examples[error_key]
            else:
                for example in examples['examples']:
                    if example_key in example:
                        word_example = example[example_key]
                        break
        except Exception as exc:
            word_example = "Exception: " + str(exc)
        return word_example

    async def get_word_definition_and_example(self, word: str) -> WordResult:
        """Queue and execute definition + examples fetches. Store in WordResult object."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            tasks.append(asyncio.create_task(
                self.get_words_api_definition(word, session)))
            tasks.append(asyncio.create_task(
                self.get_wordnik_api_example(word, session)))
            results = await asyncio.gather(*tasks)
            word_result = WordResult(
                definition=results[0], example=results[1])
            return word_result

    async def fetch(self, url: str, headers: dict, session: aiohttp.ClientSession) -> dict:
        """Helper method for async request/response within session."""
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


'''
Code below for debugging:
'''
# wordnik_result = asyncio.run(
#     WordClient().get_word_definition_and_example('prestidigation'))
# print(wordnik_result.definition)
# print(wordnik_result.example)
