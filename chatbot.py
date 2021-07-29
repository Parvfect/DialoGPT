from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_tokenizer_and_model(model = 'microsoft/DialoGPT-large'):
    """ Load tokenizer and model """
    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model)
    model = AutoModelForCausalLM.from_pretrained(model)
   
    return tokenizer, model

def generate_response(tokenizer, model, chat_round, chat_history_ids):
    """ Generate response to a given user input """
    
    new_input_ids = tokenizer.encode(input(">> You:") + tokenizer.eos_token, return_tensors='pt')

    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_round > 0 else new_input_ids

    chat_history_ids = model.generate(bot_input_ids, max_length=1250, pad_token_id=tokenizer.eos_token_id)

    print("DialoGPT: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

    return chat_history_ids

def chat_for_n_rounds(n):
    """ Chat for n rounds """
    
    tokenizer, model = load_tokenizer_and_model()
    chat_history_ids = None
    
    for chat_round in range(n):
        chat_history_ids = generate_response(tokenizer, model, chat_round, chat_history_ids)


if __name__ == '__main__':
  chat_for_n_rounds(100)
    