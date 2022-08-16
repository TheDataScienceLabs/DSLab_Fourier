"""
When you press a button, play a WAV file from memory.

Put the file EduardKhil.wav onto the Pico before running.

Sound plays when you press button A.

Refer to readme.md for wiring.
"""

from machine import I2S
from machine import ADC, Pin
from ulab import numpy as np


button_A = Pin(16, Pin.IN, Pin.PULL_UP)
button_B = Pin(17, Pin.IN, Pin.PULL_UP)

SAMPLE_RATE_IN_HZ = 22_050
SAMPLE_SIZE_IN_BITS = 16

audio_out = I2S(
    0,
    sck=Pin(18),
    ws=Pin(19),
    sd=Pin(20),
    mode=I2S.TX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=I2S.MONO,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=2000,
)



try:
    wav = open('EduardKhil.wav', "rb")
    wav_samples = bytearray(1000)
    wav_samples_mv = memoryview(wav_samples)
    num_read = 0
    while True:
        if not button_A.value():
            num_read = wav.readinto(wav_samples_mv)
            if num_read == 0:
                wav.seek(44)
            else:
                audio_out.write(wav_samples_mv[:num_read])

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

wav.close()
audio_out.deinit()
print("Done")
