""" 
Extracts lines of conversation from the json files that you get from downloading from facebook
"""


import pandas as pd

import json


input_file_location = 'message.json'

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

with open (output_file, 'w') as f:
    for i in range(len(conversation) - 1, 0, -1):
        f.write(conversation[i] + '\n')

f.close()

