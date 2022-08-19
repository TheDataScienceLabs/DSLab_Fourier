"""
A working theremin, using asyncronous functions.
"""
from machine import ADC, I2S, Pin, time_pulse_us
import math
import time
from ulab import numpy as np
import uasyncio as asyncio


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
        tone = bytes(100)

        async def write_tone():
            nonlocal tone
            swriter = asyncio.StreamWriter(audio_out)
            while True:
                swriter.write(tone)
                await swriter.drain()

        async def refresh_tone():
            nonlocal tone
            while True:
                await asyncio.sleep(0.01)
                distance = ultrasonic.read_cm()
                if math.isnan(distance):
                    continue
                samplecount = int(25 + (84 - 25) * (distance - 1) / (60 - 1))
                volume = potentiometer.read_u16() / 2
                tone = make_tone(samplecount, volume)

        asyncio.run(asyncio.gather(write_tone(), refresh_tone()))
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
