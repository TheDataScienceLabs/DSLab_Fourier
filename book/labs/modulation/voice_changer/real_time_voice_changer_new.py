#!/usr/bin/env python

"""real_time_voice_changer.py: Changes your voice in real time using SoundDevice"""

__author__ = "Mo Chen"

import sounddevice as sd
import numpy as np
import sys

# Parameters for real-time audio processing
CHUNK = 253 * 3  # Buffer size
FORMAT = 'int16'  # Sample format (16-bit PCM)
CHANNELS = 1  # Number of audio channels
RATE = 41000  # Sampling rate

# Create a **modulating** sinusoidal wave
y = (2**4) * np.sin(np.linspace(0, 6 * np.pi, CHUNK, endpoint=False))

# Real-time audio processing function
def callback(indata, outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    # Convert input to NumPy array (already int16 format)
    audio_data = indata[:, 0]  # Extract single channel
    
    # Apply modulation effect (multiplication by sinusoidal wave)
    modulated_data = np.multiply(y, audio_data).astype(np.int16)

    # Reshape and send to output
    outdata[:, 0] = modulated_data

# Open a real-time input-output audio stream
with sd.Stream(samplerate=RATE, blocksize=CHUNK, channels=CHANNELS,
               dtype=FORMAT, callback=callback):
    print("*************************************")
    print("*******   Real-Time Voice Changer   *******")
    print("*************************************")
    input("Press Enter to stop...")  # Keeps the program running

print("* Voice changer stopped.")
