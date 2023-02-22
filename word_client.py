import asyncio
import aiohttp
import config


class WordResult:
    """Used for storing results of wordnik fetches into consumable object."""

    def __init__(self, definition: str, example: str):
        self.definition = definition
        self.example = example


class WordClient:
    """Client for interacting with the WordsAPI."""

    headers = config.headers
    words_api_base_url = "https://wordsapiv1.p.rapidapi.com/words/"

    async def get_word_definition(self, word: str, session: aiohttp.ClientSession):
        """Fetch definition of provided word from WordsAPI."""
        url = self.words_api_base_url + f"{word}/definitions"
        word_def = "No definition found."
        try:
            definitions_response = await self.fetch(url, self.headers, session)
            definitions = definitions_response.get('definitions')
            if definitions is not None:
                for definition in definitions:
                    word_def = definition['definition']
                    break
        except Exception as exc:
            word_def = "Exception: " + str(exc)
        return word_def

    async def get_word_example(self, word: str, session: aiohttp.ClientSession):
        """Fetch example of provided word. Try 3 of wordnik's dictionaries."""
        url = self.words_api_base_url + f"{word}/examples"
        word_example = "No example found."
        try:
            examples_response = await self.fetch(url, self.headers, session)
            examples = examples_response.get('examples')
            if len(examples) > 0:
                word_example = examples[0]
        except Exception as exc:
            word_example = "Exception: " + str(exc)
        return word_example

    async def get_word_definition_and_example(self, word: str) -> WordResult:
        """Queue and execute definition + examples fetches. Store in WordnikResult object."""
        async with aiohttp.ClientSession() as session:
            tasks = []
            tasks.append(asyncio.create_task(
                self.get_word_definition(word, session)))
            tasks.append(asyncio.create_task(
                self.get_word_example(word, session)))
            results = await asyncio.gather(*tasks)
            word_result = WordResult(
                definition=results[0], example=results[1])
            return word_result

    async def fetch(self, url: str, headers: dict, session: aiohttp.ClientSession) -> dict:
        """Helper method of async request/response within session."""
        async with session.get(url=url, headers=headers) as response:
            return await response.json()


# Code below for debugging:
# wordnik_result = asyncio.run(WordnikClient().get_word_definition_and_example('parsimony'))
# print(wordnik_result.definition)
# print(wordnik_result.example)
