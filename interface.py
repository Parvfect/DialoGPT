
"""
The interface where 
Transcription is done and then deyaled until the
responses are sent to tts and then to Dialo GPT
and then continued for an end to end conversational Chatbot 
"""

import chatbot as cb

def feed_response():

    response = transcribe_one_response()
    return transcribe_one_response

def main():
    print(cb.talk_from_external("Do you like eating apples?", 0))
