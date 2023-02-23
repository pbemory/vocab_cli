import csv
import os
import random
import sys
from datetime import datetime, date, timedelta
import asyncio
from word_client import WordClient


def main():
    """main's tasks: give a status report (based on read_history); run the vocab exercise."""
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-wb':
        word_bank_path = args[1]
    else:
        word_bank_path = 'word_bank.csv'
    words_learned_this_week = read_history()
    run_vocab_exercise(word_bank_path, words_learned_this_week)


def read_history() -> int:
    """status_db.csv stores words learned this week (since Sunday) + 
    stores last time run_vocab_exercise saved, 
    which tells us to reset the word count (if the app hasn't run this week) 
    or preserve the word count...
    """
    if date.weekday(datetime.now()) == 6:
        most_recent_sunday = date.today()
    else:
        most_recent_sunday = date.today() - timedelta(date.weekday(datetime.now())+1)
    with open('status_db.csv', 'r', encoding='UTF-8') as status_db:
        db_reader = csv.reader(status_db)
        last_checked_sunday = date.fromisoformat(next(db_reader)[1])
        if most_recent_sunday > last_checked_sunday:
            words_learned_this_week = 0
            next(db_reader)
        else:
            words_learned_this_week = int(next(db_reader)[1])
        words_remaining = int(next(db_reader)[1])
    status_db.close()
    print(
        f"{words_learned_this_week} word{'s'[:words_learned_this_week^1]} learned this week of {words_remaining} word{'s'[:words_remaining^1]} remaining...")
    return words_learned_this_week


def run_vocab_exercise(word_bank_path: str, words_learned_this_week: int) -> None:
    """Read from the existing word bank, while creating a new, writable word bank. 
    The new word bank is temporarily appended with '_temp', until saving and overwriting the old word bank.
    Get word definitions and examples through WordnikClient.
    Save status to status_db.csv.
    """
    leveled_up_words = 0
    words_left = 0
    with open(word_bank_path, 'r', encoding='UTF-8') as csvfile:
        rows = csvfile.readlines()
        random.shuffle(rows)
        reader = csv.reader(rows)
        new_word_bank = open(word_bank_path.replace(
            '.csv', '_temp'), 'w', encoding='UTF-8')
        writer = csv.writer(new_word_bank)
        user_quit = False
        for row in reader:
            if user_quit is True:
                writer.writerow(row)
                if int(row[1].strip()) == 0:
                    words_left += 1
            else:
                if int(row[1].strip()) == 1:
                    writer.writerow(row)
                else:
                    word = row[0].strip()
                    try:
                        word_result = asyncio.run(
                            WordClient().get_word_definition_and_example(word))
                        word_prompt = input(
                            f"What word means '{word_result.definition}'? ")
                        if word_prompt == 'q':
                            writer.writerow(row)
                            words_left += 1
                            user_quit = True
                        if user_quit is False:
                            print(
                                f"********\nExample: '{word_result.example}'\n********")
                            if word_prompt == word:
                                row = level_up_word(row)
                                leveled_up_words += 1
                                words_learned_this_week += 1
                                print(
                                    f"'{word}' leveled up! {leveled_up_words} word{'s'[:leveled_up_words^1]} learned so far ...\n****")
                            else:
                                words_left += 1
                                print(
                                    f"'{word_prompt}' did not match '{word}'.\n****")
                            writer.writerow(row)
                    except Exception as exc:
                        writer.writerow(row)
                        words_left += 1
                        print(f"Something went wrong for '{word}'")
                        print("Exception: " + str(exc))
        new_word_bank.close()
    csvfile.close()
    save(words_learned_this_week, words_left)
    os.remove(word_bank_path)
    os.rename(word_bank_path.replace('.csv', '_temp'), word_bank_path)


def save(words_learned_this_week: int, words_left: int) -> None:
    """
    Save progress to status_db.csv
    """
    if date.weekday(datetime.now()) == 6:
        most_recent_sunday = date.today()
    else:
        most_recent_sunday = date.today() - timedelta(date.weekday(datetime.now())+1)
    with open('status_db.csv', 'w', encoding='UTF-8') as status_db:
        writer = csv.writer(status_db)
        writer.writerow(
            ["Date of last checked Sunday", str(most_recent_sunday)])
        writer.writerow(["Words learned since Sunday",
                        str(words_learned_this_week)])
        writer.writerow(["Words remaining", str(words_left)])
    status_db.close()


def level_up_word(csv_row: list) -> list:
    """
    Increment word score column when word is correct in run_vocab_exercise
    """
    word_level_number = int(csv_row[1])
    word_level_number += 1
    new_row = [csv_row[0], " " + str(word_level_number)]
    return new_row


if __name__ == '__main__':
    main()
