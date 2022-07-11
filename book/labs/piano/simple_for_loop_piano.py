# The MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

# Purpose:  Play a pure audio tone out of a speaker or headphones
#
# - write audio samples containing a pure tone to an I2S amplifier or DAC module
# - tone will play continuously in a loop until
#   a keyboard interrupt is detected or the board is reset
#
# Blocking version
# - the write() method blocks until the entire sample buffer is written to I2S

import os
import math
import struct
from machine import I2S
from machine import Pin
import time

def make_tone(rate, bits, frequency):
    # create a buffer containing the pure tone samples
    samples_per_cycle = rate // frequency
    sample_size_in_bytes = bits // 8
    samples = bytearray(samples_per_cycle * sample_size_in_bytes)
    volume_reduction_factor = 4
    range = pow(2, bits) // 2 // volume_reduction_factor

    format = "<h"  #need to be curious
    
    for i in range(samples_per_cycle):
        sample = range + int((range - 1) * math.sin(2 * math.pi * i / samples_per_cycle))
        struct.pack_into(format, samples, i * sample_size_in_bytes, sample)
        
    return samples

# ======= I2S CONFIGURATION =======
SCK_PIN = 16
WS_PIN = 17
SD_PIN = 18
I2S_ID = 0
BUFFER_LENGTH_IN_BYTES = 2000
# ======= I2S CONFIGURATION =======


# ======= AUDIO CONFIGURATION =======
TONE_FREQUENCY_IN_HZ = 440
SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO  # only MONO supported in this example
SAMPLE_RATE_IN_HZ = 22_050
# ======= AUDIO CONFIGURATION =======

audio_out = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.TX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

samples = make_tone(SAMPLE_RATE_IN_HZ, SAMPLE_SIZE_IN_BITS, TONE_FREQUENCY_IN_HZ)
# continuously write tone sample buffer to an I2S DAC



num_of_keys = 12
press = [0] * num_of_keys
keys = []  #to store the pin object for each key
tones = []
TONE_FREQUENCY = []

#initialize the tone table,keys
for key_numth in range(num_of_keys):
    TONE_FREQUENCY.append(int(TONE_FREQUENCY_IN_HZ * (1.059 ** (key_numth))))
    keys.append(Pin(key_numth,Pin.IN,Pin.PULL_DOWN))
    tones.append(make_tone(SAMPLE_RATE_IN_HZ, SAMPLE_SIZE_IN_BITS, TONE_FREQUENCY[key_numth]))

#to store whether the button has been pushed down
try:
    while True:
        # update the push value,the front key has higher priority
        for key_numth in range(num_of_keys):
            press[key_numth] = keys[key_numth].value()    #for combine multiple keys
            if (press[key_numth] == 1):
                audio_out.write(tones[key_numth])
                break
            
                   
                    
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

# cleanup
audio_out.deinit()
print("Done")

