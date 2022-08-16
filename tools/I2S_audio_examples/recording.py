"""
Press one button to record some audio, press another to play it back.

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

audio_in = I2S(
    1,
    sck=Pin(13),
    ws=Pin(14),
    sd=Pin(15),
    mode=I2S.RX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=I2S.MONO,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=2000,
)


try:
    record_duration_seconds = 2
    storage = bytearray(2*record_duration_seconds*SAMPLE_RATE_IN_HZ)
    while True:
        if not button_A.value():
            print('recording...', end='')
            audio_in.readinto(storage)
            print('done!')
        elif not button_B.value():
            print('playing...', end='')
            audio_out.write(storage)
            print('done!')

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

audio_out.deinit()
audio_in.deinit()
print("Done")