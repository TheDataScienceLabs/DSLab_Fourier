import machine
import time

sensor_temp = machine.ADC(machine.ADC.CORE_TEMP)

conversion_factor = 3.3 / (65535)
file = open("temp.txt", "w")
num = 12

while num>0:
  reading = sensor_temp.read_u16() * conversion_factor
  temperature = 27 - (reading - 0.706)/0.001721
  file.write(str(temperature) + "\n")
  num -= 1
  time.sleep(0.25)

file.close()