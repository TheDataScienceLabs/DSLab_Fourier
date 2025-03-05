#!/usr/bin/env python

"""megaphone.py: Captures audio using a microphone and outputs it through a speaker in real-time.
This code demonstrates how to gather audio in chunks and process it."""

__author__ = "Mo Chen"

import sounddevice as sd
import numpy as np

# Parameters for real-time audio streaming
CHUNK = 512  # Buffer size (same as before)
FORMAT = 'int16'  # Sample format (16-bit PCM)
CHANNELS = 1  # Number of channels
RATE = 41000  # Sampling rate

# Function to process audio in real-time
def callback(indata, outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    
    # Convert audio to NumPy array (already int16)
    outdata[:] = indata  # Pass input directly to output (megaphone effect)

# Open a real-time input-output audio stream
with sd.Stream(samplerate=RATE, blocksize=CHUNK, channels=CHANNELS,
               dtype=FORMAT, callback=callback):
    print("*************************************")
    print("*******   Live Megaphone On   *******")
    print("*************************************")
    input("Press Enter to stop...")  # Keeps the program running

print("* Megaphone stopped.")
