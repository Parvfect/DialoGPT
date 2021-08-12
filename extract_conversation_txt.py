""" 
Extracts lines of conversation from exported whatsapp data files 
"""

import re
import json
import uuid 



input_file_location = 'message_1.json'
conversation = []
def extract(input_file_location):
    """Extracts conversation from txt file"""
    with open(input_file_location, 'r') as f:
        data = f.readlines()
    
    f.close()
    
    dialogue = ""
    prev_person = ""
    for line in data:

        person = check_person(line)
        line = clean_line(line)
       
        if line == "":
            continue
        
        if person != prev_person:
            conversation.append(dialogue)
            dialogue = ""
        
        prev_person = person

        if line!= '':
            dialogue += line + '.'
        else: 
            dialogue += line

    write_conversation_to_file()

def check_person(line):
    """Checks the owner of the line"""
    
    return 1 if line.find('Parv') != -1 else 0
    

def clean_line(line):
    """Cleans the line"""

    return clean_known_errors(remove_special_symbols(remove_filler_text(line)))
    
    
def remove_special_symbols(line):
    """Removes special symbols"""

    return re.sub(r"[^a-zA-Z0-9.,? ]","",line)


def write_conversation_to_file():
    
    output_file = 'datasets/{}'.format(generate_unique_id() + '.txt')

    f = open(output_file, 'w')
    for i in range(0, len(conversation) - 1):
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

def remove_filler_text(line):
    """ Removes owner of string and non dialogues """
    
    if check_person(line) == 1:
        loc = line.find('Parv')
        return line[loc + 4:]
    else:   
        loc = line.find('Saurav')
        return line[loc + 6:]
    
def generate_unique_id():
    """ Return unique id for dataset"""
    return uuid.uuid4().hex[:6].upper()

def reverse_array(arr):
    return arr[::-1]


if __name__ == '__main__':
    extract(input_file_location)