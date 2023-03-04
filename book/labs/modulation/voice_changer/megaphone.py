
#!/usr/bin/env python

"""megaphone.py: Captures audio using microphone and outputs through a speaker in almost real time.
This code illustrates how to gather audio data as chunk and to act on it."""

__author__      = "Adharsh Sabukumar"

import pyaudio
import sys
import numpy as np
import wave
import audioop
import struct
import scipy.fftpack as fft

chunk = 512
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


while(True):

    data = stream.read(chunk, exception_on_overflow = False)
    data = np.array(wave.struct.unpack("%dh"%(len(data)/swidth), data))


    chunkout = struct.pack("%dh"%(len(data)), *list(data)) #convert back to 16-bit data

    stream.write(chunkout, chunk)




print ("* done")

stream.stop_stream()
stream.close()
p.terminate()
