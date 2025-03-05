#!/usr/bin/env python

"""play_audio.py: A simple script to play a recorded WAV file using SoundDevice."""

import sounddevice as sd
import soundfile as sf

# Define the file to play
INPUT_FILE_NAME = "my_recording.wav"

# Load the audio file using SoundFile
audio_data, samplerate = sf.read(INPUT_FILE_NAME)

# Indicate that playback is starting
print("*************************************")
print(f"Playing {INPUT_FILE_NAME}...")
print("*************************************")

# Play the audio using SoundDevice
sd.play(audio_data, samplerate)
sd.wait()  # Wait until playback is finished

# Indicate that playback has completed
print("******   Playback completed   ******")
