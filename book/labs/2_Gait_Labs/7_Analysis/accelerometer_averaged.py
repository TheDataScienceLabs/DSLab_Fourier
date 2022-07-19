from machine import Pin, I2C
from lsm9ds0 import LSM9DS0
import time
from averager_solution import Averager

i2c = I2C(id=1, sda=Pin(18), scl=Pin(19), freq=3_400_000)
lsm = LSM9DS0(i2c = i2c, a_sens=16)

samples = 50
av_x = Averager(samples)
av_y = Averager(samples)
av_z = Averager(samples)

av_a = Averager(samples)
av_b = Averager(samples)
av_c = Averager(samples)

filea = open("test_accel.txt", "w")
fileg = open("test_gyro.txt", "w")

while True:
    x, y, z = lsm.accel.all()
    a, b, c = lsm.gyro.all()
    av_x.append(x)
    av_y.append(y)
    av_z.append(z)
    av_a.append(a)
    av_b.append(b)
    av_c.append(c)
    filea.write('{} {} {}\n'.format(av_x.get(),av_y.get(),av_z.get()) )
    fileg.write('{} {} {}\n'.format(av_a.get(),av_b.get(),av_c.get()) )
    print(f'x:{av_x.get(): .5f}')
    time.sleep(0.01)