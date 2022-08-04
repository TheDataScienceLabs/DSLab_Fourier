"""
Demonstrates making sounds in real time, i.e. not ahead of time.
To do this, we use an interrupt.
This strategy lets us generate more sounds than we could store in memory,
so we can use the potentiometer to vary them continuously.

Only plays sound while button A is pressed.

Refer to readme.md for wiring.
"""

from machine import I2S
from machine import ADC, Pin
import time
from ulab import numpy as np


button_A = Pin(16, Pin.IN, Pin.PULL_UP)
button_B = Pin(17, Pin.IN, Pin.PULL_UP)
potentiometer = ADC(Pin(26))

SAMPLE_RATE_IN_HZ = 22_050
SAMPLE_SIZE_IN_BITS = 16

audio_out = I2S(
    0,
    sck=Pin(10),
    ws=Pin(11),
    sd=Pin(12),
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


def make_tone(frequency, waveform=lambda t: np.sin(2 * np.pi * t), amplitude=0.5, num_cycles=1):
    """
    The frequency is rounded so as to give a whole number of samples/period.
    The waveform takes a number [0,1] and produces a number [-1, 1]
    """
    num_samples = int(num_cycles*SAMPLE_RATE_IN_HZ / frequency)
    t = np.linspace(0, num_cycles, num_samples, endpoint=False)
    y = (2 ** 15 * amplitude) * waveform(t-np.floor(t))
    return np.asarray(y, dtype=np.int16).tobytes()


try:
    empty = bytes(100)
    current_tone = empty
    def callback(a):
        if button_A.value():
            a.write(empty)
        else:
            a.write(current_tone)
    audio_out.irq(callback)
    callback(audio_out)
    while True:
        current_frequency = 220*(1+2*potentiometer.read_u16()/2**16)
        current_tone = make_tone(current_frequency, amplitude=0.1)
        time.sleep(0.01)

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))
    
audio_out.deinit()
audio_in.deinit()
print("Done")