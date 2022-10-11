from typing import List

class StrPractice:

  def __init__(self,description):
    self.description = description

  def split(self,delimited_str:str,delimiter:str)->List[str]:
    return delimited_str.split(delimiter)

  def join(self,list_of_strings:List[str],delimiter:str)->str:
    return delimiter.join(list_of_strings)

str_practice_instance = StrPractice("This is the description")

str_with_commas = "aaa,bbb,ccc"
what_split_does = str_practice_instance.split(str_with_commas,",")
what_join_does = str_practice_instance.join(what_split_does,"+")
print(what_split_does)
print(what_join_does)



