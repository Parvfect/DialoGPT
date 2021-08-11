""" 
Extracts lines of conversation from the json files that you get from downloading from facebook
"""


import pandas as pd
import re
import json

input_file_location = '_chat.txt'
conversation = []
output_file = 'chat2.txt'

def from_json(input_file_location):

    # Opening JSON file
    f = open(input_file_location)
    
    name = input("Enter person")
    output_file = '{}.txt'.format(name)

    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list

    conversation = []

    for i in data['messages']:
        try:
            conversation.append(i['content'])
        except: 
            print("Exception")
    # Closing file
    f.close()


def from_txt(input_file_location):
    """Extracts conversation from txt file"""
    with open(input_file_location, 'r') as f:
        data = f.readlines()
    
    f.close()
    
    dialogue = ""
    prev_person = ""
    for line in data:

        person = check_person(line)
        line = clean_line(line)
       
        if person == prev_person:
            dialogue += line + ". "
            print(dialogue)
       
        if line == "":
            continue
       
        else : 
            conversation.append(dialogue)
            dialogue = ""

        prev_person = person
    write_conversation_to_file(output_file)

def check_person(line):
    """Checks the owner of the line"""
    
    return 1 if line.find('Parv') != -1 else 0
    


def clean_line(line):
    """Cleans the line"""

    return remove_special_symbols(remove_filler_text(line))

    
    
def remove_special_symbols(line):
    """Removes special symbols"""

    return re.sub(r"[^a-zA-Z0-9.,? ]","",line)

def remove_filler_text(line):
    """ Removes owner of string and non dialogues """
    
    if check_person(line) == 1:
        loc = line.find('Parv')
        return line[loc + 4:]
    else:   
        loc = line.find('Saurav')
        return line[loc + 6:]
    

def write_conversation_to_file(output_file):
    
    with open (output_file, 'w') as f:
        for i in range(0, len(conversation) - 1):
            f.write(conversation[i] + '\n')

    f.close()


if __name__ == '__main__':
    from_txt(input_file_location)