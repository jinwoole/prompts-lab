from google.cloud import texttospeech
import os
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

def speak(text: str):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-H",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Use BytesIO to handle the binary audio content in memory
    audio_data = BytesIO(response.audio_content)

    # Load the audio with pydub and play it
    audio = AudioSegment.from_file(audio_data, format="mp3")
    play(audio)