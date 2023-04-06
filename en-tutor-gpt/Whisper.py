# -*- coding: utf-8 -*-

import pyaudio
import wave
import openai
from pynput import keyboard
import threading



# Set up Pyaudio recording parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

def record_and_transcribe(api_key):
    # Replace with your OpenAI API key
    openai.api_key = api_key

    # Replace with your preferred model and engine ID
    model_engine = "whisper-1"

    # Define a function to start recording when 'g' is pressed
    def on_press_start(key):
        if key == keyboard.KeyCode.from_char('g'):
            return False

    # Define a function to stop recording when 'h' is pressed
    def on_press_stop(key):
        if key == keyboard.KeyCode.from_char('h'):
            return False

    # Wait for 'g' key press to start recording
    print("Press 'g' to start recording...")
    with keyboard.Listener(on_press=on_press_start) as listener:
        listener.join()

    # Start recording
    print("Recording...")
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = []

    def record():
        while not stop_recording.is_set():
            data = stream.read(CHUNK)
            frames.append(data)

    stop_recording = threading.Event()
    recording_thread = threading.Thread(target=record)
    recording_thread.start()

    # Wait for 'h' key press to stop recording
    with keyboard.Listener(on_press=on_press_stop) as listener:
        listener.join()

    stop_recording.set()
    recording_thread.join()
    print("Stopped recording.")

    # Save the recording to a WAV file
    wav_filename = "output.wav"
    with wave.open(wav_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    # Transcribe audio using OpenAI API
    with open(wav_filename, 'rb') as audio_file:
        transcript = openai.Audio.transcribe(model_engine, audio_file, language="en")
    return transcript