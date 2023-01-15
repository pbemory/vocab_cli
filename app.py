import csv, os, random, sys 
from wordnik_client import WordnikClient

'''
main's tasks:
(1) give a status report (based on read_history); 
(2) run the app.
'''
def main():
    args = sys.argv[1:]
    if len(args) == 2 and args[0] == '-wb':
        word_bank_path = args[1]
    else:
        word_bank_path = 'word_bank.csv'
    read_history()
    run_vocab_exercise(word_bank_path)

'''
read_history:
--determine last time app ran by checking last save date
--tell us how many words we've learned this week (starting from Sunday)
'''
def read_history():
    pass

'''

'''
def run_vocab_exercise(word_bank_path: str):
    leveled_up_words = 0
    wordnik_client = WordnikClient()
    with open(word_bank_path,'r') as csvfile:
        #lines = csvfile.readlines()
        reader = csv.reader(csvfile)
        new_word_bank = open(word_bank_path.replace('.csv','_temp'),'w')
        writer = csv.writer(new_word_bank)     
        quit = False
        for row in reader:
            if quit is True:
                writer.writerow(row)
            else:
                if int(row[2].strip()) == 1:
                    writer.writerow(row)
                else:
                    word = row[0].strip()
                    try:
                        word_results = wordnik_client.get_word_def_and_ex(word)
                        word_def = word_results['text']
                        word_prompt = input(f"What word means '{word_def}'? ")
                        confirm_answer_prompt = input(f"Was your word '{word}'? ")
                        if confirm_answer_prompt == 'y':
                            row = level_up_word(row)
                            leveled_up_words += 1
                            print(f"'{word}' leveled up! {leveled_up_words} word{'s'[:leveled_up_words^1]} learned so far ...")
                        writer.writerow(row)
                        if confirm_answer_prompt == 'q':
                            quit = True
                    except:
                        print(f"Wordnik couldn't find a definition for '{word}'")
        new_word_bank.close()
    csvfile.close()
    os.remove(word_bank_path)
    os.rename(word_bank_path.replace('.csv','_temp'),word_bank_path)

def level_up_word(csv_row:list) -> list:
    word_level_number = int(csv_row[2])
    word_level_number += 1
    new_row = [csv_row[0], csv_row[1], " " + str(word_level_number)]
    return new_row

if __name__ == '__main__':
    main()
