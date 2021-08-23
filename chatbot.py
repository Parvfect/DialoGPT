from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import random
import tts_gcloud as tts
from playsound import playsound

model_name = "microsoft/DialoGPT-large"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

ptr_response = []


def talk_from_internal():

    step = 0

    # chatting 5 times with greedy search
    while(True):

        # take user input
        text = feed_response()

        # encode the input and add end of string token
        input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")

        # concatenate new user input with chat history (if there is)
        bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids

        # generate a bot response
        chat_history_ids = model.generate(
            bot_input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
        )

        #print the output
        output = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        print(f"DialoGPT: {output}")

        tts.synthesize_text(output)

        # I think you can't make playsound play something if it's being called by another program?
        playsound('output.mp3')

        step = step + 1



def feed_response():

    return input("You: ")

def talk_from_external(input_text, step):
    
    # encode the input and add end of string token
    input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")

    # concatenate new user input with chat history (if there is)
    #bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if step > 0 else input_ids

    # generate a bot response
    chat_history_ids = model.generate(
        input_ids,
        max_length=1000,
        pad_token_id=tokenizer.eos_token_id,
    )

    #print the output
    output_text = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return output_text


def generate_text():
    
    nouns = ("puppy", "car", "rabbit", "girl", "monkey")
    verbs = ("runs", "hits", "jumps", "drives", "barfs") 
    adv = ("crazily.", "dutifully.", "foolishly.", "merrily.", "occasionally.")
    adj = ("adorable", "clueless", "dirty", "odd", "stupid")
    num = random.randrange(0,5)
    return nouns[num] + ' ' + verbs[num] + ' ' + adv[num] + ' ' + adj[num]

if __name__ == "__main__":
    talk_from_internal()
