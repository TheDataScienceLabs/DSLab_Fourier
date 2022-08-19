"""
Make a rudimentary theremin. This code does not work,
for reasons which are explained in the associated lab.
This version goes slightly faster by using numpy broadcasting.
"""
from machine import ADC, I2S, Pin, time_pulse_us
import math
import time
from ulab import numpy as np


def main():
    potentiometer = ADC(Pin(26))
    ultrasonic = Ultrasonic(Pin(19, Pin.OUT), Pin(20, Pin.IN))

    audio_out = I2S(
        0,
        sck=Pin(16),
        ws=Pin(17),
        sd=Pin(18),
        mode=I2S.TX,
        bits=16,
        format=I2S.MONO,
        rate=22_050,
        ibuf=2000,
    )
    try:
        while True:
            distance = ultrasonic.read_cm()
            if math.isnan(distance):
                continue
            samplecount = int(25 + (84 - 25) * (distance - 1) / (60 - 1))
            volume = potentiometer.read_u16() / 2
            tick = time.ticks_us()
            tone = make_tone(samplecount, volume)
            tock = time.ticks_us()
            print(f"the tone took {tock-tick} microseconds to compute.")

            audio_out.write(tone)
    finally:
        audio_out.deinit()


def make_tone(samplecount, volume):
    tone = volume * np.sin(np.linspace(0, 2 * np.pi, samplecount, endpoint=False))
    return np.asarray(tone, dtype=np.int16).tobytes()


class Ultrasonic:
    """
    Interface for an HCSR04 ultrasonic distance sensor.
    Configure trig as an output, and echo as in input.
    """

    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        self.trig.off()

    def read_ul(self):
        """
        Measure the distance as a unitless quantity.
        """
        self.trig.on()
        time.sleep_us(10)
        self.trig.off()
        return time_pulse_us(self.echo, 1, 4000)

    def read_cm(self):
        """
        Measure the distance then convert to centimeters.
        """
        ul = self.read_ul()
        if ul > 0:
            return ul / 58
        else:
            return float("nan")


if __name__ == "__main__":
    main()
