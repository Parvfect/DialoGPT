from IPython.display import clear_output
import logging

def new_dialogue():

  global conditioned_tokens
  global generated_tokens
  conditioned_tokens = []; generated_tokens = []
  reinput("What is the meaning of life?")
  generate()

  while True:
    cmd = input()

    if cmd == "reset":
      clear_output()
      new_dialogue()
      break

    if cmd != "":	
      reinput(cmd)
    generate()
    
new_dialogue()