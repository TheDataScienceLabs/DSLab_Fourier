import time
import math
from machine import Pin, I2C
from lsm9ds0 import LSM9DS0
from ssd1306 import SSD1306_I2C
from averager_solution import Averager


def main():
    i2c = I2C(id=1, sda=Pin(18), scl=Pin(19), freq=3_400_000)
    led = Pin(25, Pin.OUT)
    button = Pin(3, Pin.IN, Pin.PULL_UP)
    inclinometer = Inclinometer(i2c, button, led)
    while True:
        inclinometer.write()
        for i in range(50):
            inclinometer.read()
        
    
class Inclinometer:
    def __init__(self, i2c, button, led, samples = 500):
        self.display = Display(i2c)
        self.accelerometer = LSM9DS0(i2c = i2c, a_sens=16)
        self.button = button
        self.led = led
        self.x = Averager(samples)
        self.y = Averager(samples)
        self.z = Averager(samples)
        
    def read(self):
        x, y, z = self.accelerometer.accel.all()
        self.x.append(x)
        self.y.append(y)
        self.z.append(z)
        
    def write(self):
        if self.button.value():
            x = self.x.get()
            y = self.y.get()
            z = self.z.get()
            theta = math.atan2(x, y)*180/math.pi
            self.display.update(x, y, z, theta)
            self.led.value(abs(z)<0.01)
        else:
            self.display.hold()
        

class Display(SSD1306_I2C):
    def __init__(self, i2c):
        super().__init__(128, 64, i2c)
        self.fill(0)
        self.text('loading...', 0, 0, 1)
        self.show()
        
    def update(self, x, y, z, theta):
        self.fill(0)
        self.text(f"x:{x: .3f}", 0, 10, 1)
        self.text(f"y:{y: .3f}", 0, 20, 1)
        self.text(f"z:{z: .3f}", 0, 30, 1)
        self.text(f"O:{theta: 5.1f}", 0, 40, 1)
        self.text("-", 0, 40, 1)
        self.show()
        
    def hold(self):
        self.fill_rect(0, 0, 32, 9, 1)
        self.text("HOLD", 0, 1, 0)
        self.show()
        
        
if __name__ == '__main__':
    main()