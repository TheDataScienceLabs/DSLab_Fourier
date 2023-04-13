from machine import Pin, I2C
from lsm9ds0 import LSM9DS0
import time
from averager_solution import Averager

i2c = I2C(id=1, sda=Pin(18), scl=Pin(19), freq=3_400_000)
lsm = LSM9DS0(i2c = i2c, a_sens=16)

samples = 10

av_x = Averager(samples)
av_y = Averager(samples)
av_z = Averager(samples)

filea = open("test_accel.txt", "w")

while True:
    x, y, z = lsm.accel.all()

    av_x.append(x)
    av_y.append(y)
    av_z.append(z)

    filea.write('{} {} {}\n'.format(av_x.get(),av_y.get(),av_z.get()) )
    time.sleep(0.01)
    
    
    print(f'x:{av_x.get(): .5f}')
