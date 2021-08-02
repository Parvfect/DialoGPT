"""
We will convert this dataset in a way that every response row will contain n previous responses as a context.
For our purposes, seven previous responses will be enough.


Each response has context of seven previous responses - I can do that. 
"""

from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np

conversationA = [] # First guy's responses
conversationB = [] # Second guy's responses
conversation = [] # Combined conversation with each line as an index element

context = [[]] # Each line contains n previous responses



def create_context(conversation, n)
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
response = conversation
context = create_context(conversation, number_context)
columns = ['response', 'context']
columns = columns + ['context/' + str(i) for i in range(number_context)]

df = pd.DataFrame.from_records(context, columns = columns)

# Split dataset into training and testing parts
train, test = train_test_split(df, test_size = 0.1)


# We need to convert dataset in a format suitable for our model 
# Concatenate reponses in one string for each row and add an end of string token between reponses

def construct_conv(row, tokeniser, eos = True):
    flatter = lambda l : [item for sublist in l for item in sublist]
    conv = list(reversed([tokeniser.encode(x) + [tokeniser.eos_token_id] for x in row]))
    conv = flatten(conv)
    return conv

class ConversationDataset(Dataset):

    def __init__(self, tokeniser : PreTrainedTokenizer, args, df, block_size = 512):

        block_size = block_size - (tokeniser.max_len - tokeniser.max_len_single_sentence)

        directory = args.cache_dir
        cached_features_file = os.path.join(
            directory, args.model_type + "__cached_lm_" + str(block_size)
            )

        if os.path.exists(cached_features_file) and not args.overwrite_cache :
            logger.info("Loadinf features from cached file %s", cached_features_file)
            with open(cached_features_file, "rb") as handle:
                self.examples = pickle.load(handle)
        
        else:
            logger.info("Creating features from dataset file at %s", directory)

            self.examples = []
            
            for _, row in df.iterrows():
                conv = construct_conv(row, tokeniser)
                self.examples.append(conv)

            logger.info("Saving features into cached file %s", cached_features_file)

            with open(cached_features_file, "wb") as handle:
                pickle.dump(self.examples, handle, protocol = pickle.HIGHEST_PROTOCOL)

    
    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        return torch.tensor(self.examples[item], dtype = torch.long)


# Caching and storing of data/checkpoints
