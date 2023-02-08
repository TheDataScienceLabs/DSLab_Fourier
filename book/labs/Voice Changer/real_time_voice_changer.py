#!/usr/bin/env python

"""real_time_voice_changer.py: As the name indicates, this code changes your voice in realtime"""

__author__      = "Adharsh Sabukumar"



import pyaudio
import sys
import numpy as np
import wave
import audioop
import struct
import scipy.fftpack as fft

chunk = 253 * 3
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 41000
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = chunk)
swidth = 2

y = 2**4*np.sin(np.linspace(0, 6*np.pi, chunk, endpoint=False))

while(True):

    data = stream.read(chunk, exception_on_overflow = False)
    data_length = len(data)
    data = np.array(wave.struct.unpack("%dh"%(data_length/swidth), data))
    data_length = data_length//swidth

    data = np.multiply(y,data).astype(np.int16)

    #print(data)

    chunkout = struct.pack("%dh"%(data_length), *list(data)) #convert back to 16-bit data
    stream.write(chunkout, chunk)


print ("* done")

stream.stop_stream()
stream.close()
p.terminate()
