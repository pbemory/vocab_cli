import csv, os, random, sys
from datetime import datetime, date, timedelta
import asyncio
from wordnik_client import WordnikClient


def main():
    """main's tasks:
    (1) give a status report (based on read_history); 
    (2) run the vocab exercise.
    """
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-wb':
        word_bank_path = args[1]
    else:
        word_bank_path = 'word_bank.csv'
    words_learned_this_week = read_history()
    run_vocab_exercise(word_bank_path, words_learned_this_week)

def read_history() -> int:
    """status_db.csv (1) stores words learned this week (since Sunday); (2) stores last time run_vocab_exercise saved, which tells us to reset the word count (if the app hasn't run this week) or preserve the word count...
    """
    most_recent_sunday = date.today() - timedelta(date.weekday(datetime.now())+1)
    with open('status_db.csv','r') as status_db:
        db_reader = csv.reader(status_db)
        last_checked_sunday = date.fromisoformat(next(db_reader)[1])
        if most_recent_sunday > last_checked_sunday:
            words_learned_this_week = 0
        else:
            words_learned_this_week = int(next(db_reader)[1])
    status_db.close()
    print(f"{words_learned_this_week} word{'s'[:words_learned_this_week^1]} learned this week...")
    return words_learned_this_week

def run_vocab_exercise(word_bank_path: str, words_learned_this_week: int):
    """count words leveled up this session.
    --read from the existing word bank, while creating a new, writable word bank. The new word bank is temporarily appended with '_temp', until saving and overwriting the old word bank.
    --get word definitions and examples through WordnikClient
    --save by writing to status_db.csv
    """
    leveled_up_words = 0
    with open(word_bank_path,'r') as csvfile:
        rows = csvfile.readlines()
        total_word_count = len(rows)
        print(total_word_count)
        random.shuffle(rows)
        reader = csv.reader(rows)
        new_word_bank = open(word_bank_path.replace('.csv','_temp'),'w')
        writer = csv.writer(new_word_bank)     
        quit = False
        for row in reader:
            if quit is True:
                writer.writerow(row)
            else:
                if int(row[1].strip()) == 1:
                    writer.writerow(row)
                else:
                    word = row[0].strip()
                    try:
                        word_result = asyncio.run(WordnikClient().get_word_definition_and_example(word))
                        word_prompt = input(f"What word means '{word_result.definition}'? ")
                        if word_prompt == 'q':
                            writer.writerow(row)
                            quit = True
                        if quit is False:
                            confirm_answer_prompt = input(f"Example: '{word_result.example}'\nWas your word '{word}'? (y/n): ")
                            if confirm_answer_prompt == 'y':
                                row = level_up_word(row)
                                leveled_up_words += 1
                                words_learned_this_week += 1
                                print(f"'{word}' leveled up! {leveled_up_words} word{'s'[:leveled_up_words^1]} learned so far ...")
                            writer.writerow(row)
                            if confirm_answer_prompt == 'q':
                                quit = True
                    except Exception as e:
                        writer.writerow(row)
                        print(f"Something went wrong for '{word}'")
                        print(e)
        new_word_bank.close()
    csvfile.close()
    save(words_learned_this_week)
    os.remove(word_bank_path)
    os.rename(word_bank_path.replace('.csv','_temp'),word_bank_path)

def save(words_learned_this_week: int):
    most_recent_sunday = date.today() - timedelta(date.weekday(datetime.now())+1)
    with open('status_db.csv','w') as status_db:
        writer = csv.writer(status_db)
        writer.writerow(["Date of last checked Sunday", str(most_recent_sunday)])
        writer.writerow(["Words learned since Sunday", str(words_learned_this_week)])
    status_db.close()

def level_up_word(csv_row:list) -> list:
    word_level_number = int(csv_row[1])
    word_level_number += 1
    new_row = [csv_row[0], " " + str(word_level_number)]
    return new_row

if __name__ == '__main__':
    main()
