
import os
import openai

openai.api_key = ""

input_text = ""

def chat(prompt):
    response = openai.Completion.create(
    engine="davinci",
    prompt=prompt, 
    temperature=0.9,
    max_tokens=150,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=["\n", " Human:", " AI:"]
    )

    return response.choices[0].text


def take_input_text():
    global input_text
    input_text = input("Human: ")
    return input_text



def chat_loop():
    
    prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\n "

    for i in range(100):
        take_input_text()
        
        if check_keyboard_click():
            break
        
        prompt = prompt + "Human : " + input_text + "\n"
        response = chat(prompt)
        prompt = prompt + response + "\n"
        print(response)

    
    return prompt
        

def generate_random_string():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

def save_to_file(prompt):
    random_string = generate_random_string()
    file_name = "chat_" + random_string + ".txt"
    file = open(file_name, "w")
    file.write(prompt)
    file.close()
    print("File saved as " + file_name)

prompt = chat_loop()
save_to_file(prompt)