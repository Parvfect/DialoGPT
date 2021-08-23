import soundfile as sf
from nemo.collections.tts.models.base import SpectrogramGenerator, Vocoder
import tensorflow as tf

# Download and load the pretrained tacotron2 model
spec_generator = SpectrogramGenerator.from_pretrained("tts_en_tacotron2")

# Download and load the pretrained waveglow model
vocoder = Vocoder.from_pretrained("tts_waveglow_88m")

# All spectrogram generators start by parsing raw strings to a tokenized version of the string
parsed = spec_generator.parse("Saurav is a whore")

# Then take the tokenized string and produce a spectrogram
spectrogram = spec_generator.generate_spectrogram(tokens=parsed)
# Finally, a vocoder converts the spectrogram to audio
audio = vocoder.convert_spectrogram_to_audio(spec=spectrogram)

# Save the audio to disk in a file called speech.wav
sf.write("speech.wav", audio.to('cpu').numpy().T, 22050)