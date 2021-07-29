"""
Shamelessly copy pasted from - https://colab.research.google.com/drive/1SETfvx_ot_-VhDXjwik2SxundaQZ9rDI#scrollTo=RZd4iXX5SqKC
which I found under - https://www.reddit.com/r/MachineLearning/comments/dt5woy/p_dialogpt_state_of_the_art_conversational_model/
"""


import os
import torch
import torch.nn.functional as F
from transformers import GPT2Tokenizer, GPT2LMHeadModel, GPT2Config
import numpy as np

"""
Pre scripting actions 
import os
!wget https://convaisharables.blob.core.windows.net/lsp/multiref/medium_ft.pkl
if not os.path.exists("DialoGPT"):
  !git clone https://github.com/microsoft/DialoGPT.git
"""

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
weights = torch.load('medium_ft.pkl')
# cfg = GPT2Config(n_embd=1024,n_layer=24,n_head=16)
cfg = GPT2Config.from_json_file('DialoGPT/configs/345M/config.json')
model = GPT2LMHeadModel(cfg)

# fix misused key value
weights["lm_head.weight"] = weights["lm_head.decoder.weight"]
weights.pop("lm_head.decoder.weight",None)

model.load_state_dict(weights)
model.eval()
model.to('cuda')

conditioned_tokens = []
generated_tokens = []

def reinput(text):
	global conditioned_tokens
	os.system('cls' if os.name == 'nt' else 'clear')
	
	# print((conditioned_tokens))
	# conditioned_tokens = np.asarray(conditioned_tokens)
	# conditioned_tokens = np.where(conditioned_tokens == 50256,tokenizer.encode("\n")[0],conditioned_tokens)

	conditioned_tokens += tokenizer.encode("\t" + text) + [50256] # Append operator to prepend conversation history
	print("Me: " + text + "\n" + "Bot: ",end='')



def top_p_filtering(logits, top_p=0.9, filter_value=-float('Inf')):
  """
  Credit: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
  """
  assert logits.dim() == 1  # batch size 1 for single word generation
  sorted_logits, sorted_indices = torch.sort(logits, descending=True)
  cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
  # remove tokens with cumulative probability above the threshold
  sorted_indices_to_remove = cumulative_probs > top_p
  # shift the indices to the right to keep also the first token above the threshold
  sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
  sorted_indices_to_remove[..., 0] = 0
  indices_to_remove = sorted_indices[sorted_indices_to_remove]
  logits[indices_to_remove] = filter_value
  return logits


def recalc():
	global conditioned_tokens
	global generated_tokens
  # for segment display purpose, keep 2 sets of tokens
	indexed_tokens = conditioned_tokens + generated_tokens
  

# 	if len((indexed_tokens)) > 128:
# 	  indexed_tokens = indexed_tokens[len(indexed_tokens)-128:]

	tokens_tensor = torch.tensor([indexed_tokens])
  
	tokens_tensor = tokens_tensor.to('cuda')
	with torch.no_grad():
	    outputs = model(tokens_tensor)
	    predictions = outputs[0]
	logits = predictions[0, -1, :]
	filtered_logits = top_p_filtering(logits)
	probabilities = F.softmax(filtered_logits, dim=-1)
	next_token = torch.multinomial(probabilities, 1)
	generated_tokens.append(next_token.item())
	return next_token.item()

def generate():
	global conditioned_tokens
	global generated_tokens
  
	if len(tokenizer.decode(conditioned_tokens)) > 320:
	  dc = tokenizer.decode(conditioned_tokens)
	  dc = dc[len(dc)-320:]
	  idx = dc.find("<|endoftext|>")
	  if idx != -1:
	    dc = dc[idx+len("<|endoftext|>"):]
# 	  print("exceeded = " + dc)
# 	  print("</exceeded>")
	  conditioned_tokens = tokenizer.encode(dc)
  
	while True:
		result = recalc()

		if result == 50256:
      # end-of-text : 50256
      # use this special token to split segments

			decoded_reply = tokenizer.decode(generated_tokens)

			to_print = decoded_reply
			if to_print.endswith("<|endoftext|>"):
			  to_print = to_print[:-len("<|endoftext|>")]
			print(to_print)
			
      # Uncomment to debug (print) conversation history that is re-fed to the model
# 			cond_str = tokenizer.decode(conditioned_tokens[:-1])
# 			cond_str = cond_str.replace("<|endoftext|>","\n") # Since "<end-of-text> (50256)" is mapped to the newline character (\n) by default when calling decode():
# 			print("(condstr_dbg) " + cond_str)
# 			print(r"(/constr_dbg)")
      

			conditioned_tokens += (tokenizer.encode(decoded_reply))
    
			generated_tokens = []
			break