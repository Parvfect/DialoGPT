"""
We will convert this dataset in a way that every response row will contain n previous responses as a context.
For our purposes, seven previous responses will be enough.


Each response has context of seven previous responses - I can do that. 
"""

from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import pandas as pd
from transformers import AutoModelWithLMHead, AutoTokenizer
import torch



context = [[]] # Each line contains n previous responses


def extract_conversation(filename):
    
    conversation = []
    with open(filename, 'r') as f:
        for line in f:
            conversation.append(line[:-1])
        
    return conversation


def create_context(conversation, n):
    """ Takes a line by line response array and returns context such that each line has n previous responses in a row"""

    context = []

    for i in range(n, len(conversation)):
        row = []
        prev = i - 1 - n
        for j in range(i, prev, -1):
            row.append(conversation[j])
        context.append(row)

    return context


# Create dataframe with columns response and context
number_context = 7
context = create_context(extract_conversation('dataset.txt'), number_context)
columns = ['response', 'context']
columns = columns + ['context/' + str(i) for i in range(1,number_context)]

df = pd.DataFrame.from_records(context, columns = columns)

# Split dataset into training and testing parts
train, test = train_test_split(df, test_size = 0.1)
