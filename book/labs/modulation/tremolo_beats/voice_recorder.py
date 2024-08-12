#!/usr/bin/env python

"""voice_recorder.py: As the name indicates, this code is used to record audio"""

__author__ = "Adharsh Sabukumar"

import pyaudio
import wave

# Parameters for audio recording
chunk = 1024  # Number of frames per buffer (chunk size)
FORMAT = pyaudio.paInt16  # Format for the audio (16-bit PCM)
CHANNELS = 1  # Number of audio channels 
RATE = 44100  # Sampling rate (samples per second)
RECORD_SECONDS = 5  # Duration of the recording in seconds
OUTPUT_FILE_NAME = "my_recording.wav"  # Name of the output file

# Initialize the PyAudio object
p = pyaudio.PyAudio()

# Open a stream for recording audio
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,  # Stream is opened for input (recording)
                frames_per_buffer=chunk)  # Buffer size

frames = list()  # List to store recorded audio frames

# Indicate that recording has started
print("*************************************")
print("*******   recording started   *******")

# Loop to read and store audio data for the specified duration
for i in range(0, RATE // chunk * RECORD_SECONDS):
    frame = stream.read(chunk, exception_on_overflow=False)  # Read audio data from the stream
    frames.append(frame)  # Append the data to the frames list

# Indicate that recording has completed
print("******   recording completed   ******")
print("*************************************")

# Stop the audio stream and close it
stream.stop_stream()
stream.close()
p.terminate()  # Terminate the PyAudio session

# Indicate that the audio is being saved to a file
print("----  saving audio as .wav file  ----")
print("*************************************")

# Save the audio to a wav file 
file = wave.open(OUTPUT_FILE_NAME, 'wb') # Open a wave file for writing
file.setnchannels(CHANNELS)  # Set the number of channels
file.setsampwidth(p.get_sample_size(FORMAT))  # Set the sample width (in bytes)
file.setframerate(RATE)  # Set the sampling rate
file.writeframes(b''.join(frames))  # Write the frames to the file
file.close()  # Close the file
