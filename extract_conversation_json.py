""" 
Extracts lines of conversation from the json files that you get from downloading from facebook and instagram
"""


import pandas as pd
import re
import json
import uuid 


input_file_location = 'message_1.json'
conversation = []

def extract(input_file_location):
    """Extracts conversation from the input_file """
    


    # Opening JSON file
    f = open(input_file_location)
    

    data = json.load(f)
    dialogue = ""
    prev_person = ""

    for line in data['messages']:
        
        person = check_person(line)

        try :
            line = line['content']
        except :
            print("Exception")
            prev_person = person
            continue

        line = clean_line(line)

        if line == "":
            continue
        
        if person != prev_person:
            conversation.append(dialogue)
            dialogue = ""
        
        prev_person = person

        if line!= '':
            dialogue = line + '.' + dialogue
        else: 
            dialogue = line + dialogue

    write_conversation_to_file()

def check_person(line):
    """Checks the owner of the line"""
    
    return 1 if line['sender_name'].find('Parv') != -1 else 0
    

def clean_line(line):
    """Cleans the line"""

    return clean_known_errors(remove_special_symbols((line)))

def remove_special_symbols(line):
    """Removes special symbols"""

    return re.sub(r"[^a-zA-Z0-9.,? ]","",line)


def write_conversation_to_file():
    
    output_file = 'datasets/{}'.format(generate_unique_id() + '.txt')

    f = open(output_file, 'w')
    for i in range(len(conversation) - 1, 0, -1):
        f.write(conversation[i] + '\n')

    f.close()

def clean_known_errors(line):
    """Cleans - message is deleted, video omitted , etc """

    arr = [
        'Missed voice call',
        'video omitted',
        'This message was deleted',
        'document omitted',
        'https',
        'Missed video call',
        'http'
    ]

    for i in arr:
        if line.find(i) != -1:
            return ""

    return line


def generate_unique_id():
    """ Return unique id for dataset"""
    return uuid.uuid4().hex[:6].upper()

def reverse_array(arr):
    return arr[::-1]


if __name__ == '__main__':
    extract(input_file_location)