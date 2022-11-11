import csv, os, random, sys
import config
from wordnik_api_client import WordnikClient

'''
main's tasks:
(1) get our wordbank; 
(2) give a status report (based on read_history()); 
(3) run the app.
'''
def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-wb':
        word_bank_path = args[1]
    else:
        word_bank_path = 'word_bank.csv'

'''
read_history:
--determine last time app ran by checking last save date
--tell us how many words we've learned this week (starting from Sunday)
--don't overcomplicate--should just be since last Sunday, that 's a refactor
'''
def read_history():
    pass


def run_vocab_exercise():
    wordnik_client = WordnikClient()
    results = wordnik_client.get_def("overhang")


def save():
    pass


if __name__ == '__main__':
    main()
