from google.cloud import texttospeech
import os
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
#USE GOOGLE TTS API
def speak(text: str):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Neural2-H",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Use BytesIO to handle the binary audio content in memory
    audio_data = BytesIO(response.audio_content)
    audio = AudioSegment.from_file(audio_data, format="mp3")
    play(audio)