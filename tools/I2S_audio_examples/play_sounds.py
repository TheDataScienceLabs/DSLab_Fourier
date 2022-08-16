"""
This demonstrates the basic method of playing back sounds.
When each button is pressed, a different tone plays.
The tones are generated according to a configurable waveform.
Refer to readme.md for wiring.
"""

from machine import I2S
from machine import ADC, Pin
from ulab import numpy as np


button_A = Pin(16, Pin.IN, Pin.PULL_UP)
button_B = Pin(17, Pin.IN, Pin.PULL_UP)
potentiometer = ADC(Pin(26))

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


def make_tone(frequency, waveform=lambda t: np.sin(2 * np.pi * t), amplitude=0.5):
    """
    The frequency is rounded so as to give a whole number of samples/period.
    The waveform takes a number [0,1] and produces a number [-1, 1]
    """
    num_samples = int(SAMPLE_RATE_IN_HZ / frequency)
    t = np.linspace(0, 1, num_samples, endpoint=False)
    y = (2 ** 15 * amplitude) * waveform(t)
    return np.asarray(y, dtype=np.int16).tobytes()


try:
    middle_a = make_tone(440)
    middle_c = make_tone(262, waveform=lambda t: 4 * abs(t - 0.5) - 1)
    while True:
        if not button_A.value():
            audio_out.write(middle_a)
        elif not button_B.value():
            audio_out.write(middle_c)

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

audio_out.deinit()
audio_in.deinit()
print("Done")
