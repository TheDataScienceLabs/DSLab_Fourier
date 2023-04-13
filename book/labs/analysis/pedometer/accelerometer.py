from machine import Pin, I2C
from lsm9ds0 import LSM9DS0
import time

i2c = I2C(id=1, sda=Pin(18), scl=Pin(19), freq=3_400_000)
lsm = LSM9DS0(i2c = i2c, a_sens=16)

while True:
    x, y, z = lsm.accel.all()
    print(f'x:{x: .5f}\ty:{y: .5f}\tz:{z: .5f}')
    time.sleep(0.01)
