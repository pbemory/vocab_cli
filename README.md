# vocab_cli
  * Tiny command line tool for building vocabulary using a word bank and dictionary APIs. I use this tool when finding ten-dollar words in books.

# contents
  * app.py—runs the vocab exercise and prints progress.
  * word_client.py—fetches definitions and examples from WordsApi and Wordnik API.
  * status_db.csv—serves as a db for progress.
  * word_bank.csv—column 1: vocabulary; column 2: binary word score (0 for unlearned, 1 for learned).

# to-do
  * Package this project for install.
