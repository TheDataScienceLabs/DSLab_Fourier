from machine import Pin, I2C
from lsm9dso import LSM9DS0
import time
from averager_solution import Averager

i2c = I2C(id=1, sda=Pin(14), scl=Pin(15), freq=3_400_000)
lsm = LSM9DS0(i2c = i2c, a_sens=16)

samples = 10


av_x = Averager(samples)
av_y = Averager(samples)
av_z = Averager(samples)

filea = open("test_accel.txt", "w")

while True:
    time.sleep(10)
    x, y, z = lsm.accel.all()

    av_x.append(x)
    av_y.append(y)
    av_z.append(z)

    #filea.write('{} {} {}\n'.format(av_x.get(),av_y.get(),av_z.get()) )
    
    print(f'x:{av_x.get(): .5f}')
