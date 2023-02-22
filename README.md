# vocab-cli
  * Tiny Python tool for building vocabulary from the command line using a word bank and Words/Wordnik api. I use this tool when finding ten-dollar words in books.

# contents
  * app.py—runs the vocab exercise and prints progress.
  * word_client.py—fetches definitions and examples from Words/Wordnik api.
  * status_db.csv—serves as a db for progress.
  * word_bank.csv—column 1: vocabulary; column 2: binary word score (0 for unlearned, 1 for learned).

# to-do
  * Package this project for install.
