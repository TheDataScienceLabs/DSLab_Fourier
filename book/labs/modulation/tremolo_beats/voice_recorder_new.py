#!/usr/bin/env python

"""voice_recorder.py: A simple script to record audio using SoundDevice and save it using SoundFile."""

__author__ = "Mo Chen"

import sounddevice as sd
import soundfile as sf
import numpy as np

# Parameters for audio recording
CHUNK = 1024  # Buffer size (not used directly in sounddevice)
FORMAT = 'int16'  # Sample format (16-bit PCM)
CHANNELS = 1  # Number of audio channels
RATE = 44100  # Sampling rate (samples per second)
RECORD_SECONDS = 5  # Duration of the recording in seconds
OUTPUT_FILE_NAME = "my_recording.wav"  # Output file name

# Indicate that recording has started
print("*************************************")
print("*******   recording started   *******")

# Record audio using SoundDevice
audio_data = sd.rec(int(RECORD_SECONDS * RATE), samplerate=RATE, channels=CHANNELS, dtype=FORMAT)
sd.wait()  # Wait until recording is finished

# Indicate that recording has completed
print("******   recording completed   ******")
print("*************************************")

# Indicate that the audio is being saved to a file
print("----  saving audio as .wav file  ----")
print("*************************************")

# Save the recorded audio as a WAV file using SoundFile
sf.write(OUTPUT_FILE_NAME, audio_data, RATE)

print(f"Recording saved as {OUTPUT_FILE_NAME}")
