import os
import csv
import argparse
from vocab_cli import app, __version__


def parse_args():
    """Parse args with argparse."""
    parser = argparse.ArgumentParser(description = 'cli tool for building vocab from a word bank.')
    parser.add_argument('-v','--version', action='version', version=f"Version {__version__}")
    parser.add_argument('-wb', help='specify a path to your word_bank.')
    parser.add_argument('-a', help='Add words to the word bank as a list. E.g.: objurgate, mollify, globose')
    args = parser.parse_args()
    return args


def main():
    """Launch app with args."""
    args = parse_args()
    if (args.a != None):
        add_words(args.a)
    else:
        app.launch(args.wb)

def add_words(new_words):
    """Add words to word bank."""
    new_words_list = new_words.split(",")
    word_bank_path = os.path.join(
        os.path.dirname(__file__), 'word_bank.csv')
    with open(word_bank_path, 'a', encoding='UTF-8') as csvfile:
        writer = csv.writer(csvfile)
        for word in new_words_list:
            writer.writerow([word,0])
    csvfile.close()

if __name__ == '__main__':
    main()
