#from pydub import AudioSegment
import time
from playsound import playsound
from google.cloud import texttospeech


def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-GB-Wavenet-F",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # Response.audio_content contains the synthesized audio content, I need to play that in real time
    
    # Writing the audio content to an mp3 file

    with open("output", "wb") as out:
        out.write(response.audio_content)
    
    playsound("output.mp3")
    delay(1)

def play_sound(audio_path):

    AudioSegment.from_mp3(audio_path)
    delay(1)

def delay(duration):
    time.sleep(duration)


def real_time_tts():

    while(True):
        text = input("Enter text to synthesize: ")
        synthesize_text(text)


if __name__ == "__main__":
    real_time_tts()