import config
import asyncio
import aiohttp


class WordnikResult:
    """Used for storing results of wordnik fetches into consumable object."""

    def __init__(self, definition: str, example: str):
        self.definition = definition
        self.example = example


class WordnikClient:
    """Client for interacting with the wordnik API."""

    api_key = config.api_key
    wordnik_api_base_url = f"https://api.wordnik.com/v4/word.json/"
    params = {'api_key': api_key, 'limit': '3'}

    async def get_word_definition(self, word: str, session: aiohttp.ClientSession):
        """Fetch definition of provided word. Try 3 of wordnik's dictionaries."""
        url = self.wordnik_api_base_url + f"{word}/definitions"
        word_def = "No definition found."
        try:
            definitions = await self.fetch(url, self.params, session)
            definition_key = 'text'
            error_key = 'message'
            if error_key in definitions:
                word_def = "Error: " + definitions[error_key]
            else:
                for definition in definitions:
                    if definition_key in definition:
                        word_def = definition[definition_key]
                        break
        except Exception as exc:
            word_def = "Exception: " + str(exc)
        return word_def

    async def get_word_example(self, word: str, session: aiohttp.ClientSession):
        """Fetch example of provided word. Try 3 of wordnik's dictionaries."""
        url = self.wordnik_api_base_url + f"{word}/examples"
        word_example = "No example found."
        try:
            examples = await self.fetch(url, self.params, session)
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

    async def get_word_definition_and_example(self, word: str) -> WordnikResult:
        """Queue and execute definition + examples fetches. Store in WordnikResult object."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            tasks.append(asyncio.create_task(
                self.get_word_definition(word, session)))
            tasks.append(asyncio.create_task(
                self.get_word_example(word, session)))
            results = await asyncio.gather(*tasks)
            wordnik_result = WordnikResult(
                definition=results[0], example=results[1])
            return wordnik_result

    async def fetch(self, url: str, params: dict, session: aiohttp.ClientSession):
        """Helper method of async request/response within session."""
        async with session.get(url=url, params=params) as response:
            return await response.json()

    # Code below for debugging:
    # wordnik_result = asyncio.run(WordnikClient.get_word_definition_and_example('parsimony'))
    # print(wordnik_result.definition)
    # print(wordnik_result.example)
