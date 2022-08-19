"""
Check that the ultrasonic sensor and potentiometer
are conected correctly for building a theremin.
"""
from machine import ADC, Pin, time_pulse_us
import time


def main():
    potentiometer = ADC(Pin(26))
    ultrasonic = Ultrasonic(Pin(19, Pin.OUT), Pin(20, Pin.IN))

    while True:
        distance = ultrasonic.read_cm()
        pot_value = potentiometer.read_u16()

        print(f"{pot_value:5d}\t{distance:6.2f}")
        time.sleep(0.01)


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
