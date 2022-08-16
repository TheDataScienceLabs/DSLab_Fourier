"""
Demonstrate playing multiple simultaneous tones, which requires making samples which share a common period. These are individually computed in advance, but summed up here together.

Frequencies will not be represented exactly, so that they can line up exactly (small misalignments when repeating sounds will be audible) so we compromise by making a sample size which is small enough to fit in memory, but large enough to hold samples of everything.

Refer to readme.md for wiring.
"""


from machine import I2S
from machine import ADC, Pin
import os
import time
from ulab import numpy as np
import uasyncio as asyncio

ideal_sample_counts = [
    (1186, [14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 27]),
    (2461, [29, 31, 33, 35, 37, 39, 41, 44, 46, 49, 52, 55]),
    (5474, [65, 69, 73, 77, 82, 87, 92, 97, 103, 109, 116, 123]),
    (6749, [80, 85, 90, 95, 101, 107, 113, 120, 127, 135, 143, 151]),
    (9776, [116, 123, 130, 138, 146, 155, 164, 174, 184, 195, 207, 219]),
    (15599, [185, 196, 208, 220, 233, 247, 262, 277, 294, 311, 330, 349]),
]
letters = "C C# D D# E F F# G G# A A# B".split()


print("precomputing samples...", end="")
tick = time.ticks_us()
num_samples, note_divisors = ideal_sample_counts[1]
filenames = [f"{num_samples}/{letter}.npy" for letter in letters]
if str(num_samples) not in os.listdir():
    t = np.linspace(0, 2 * np.pi, num_samples, endpoint=False)
    os.mkdir(str(num_samples))
    for filename, divisor in zip(filenames, note_divisors):
        np.save(filename, np.sin(t * divisor))
    del(t)
else:
    print('found some ready made!...', end='')
play_buffer = np.zeros(num_samples, dtype=np.int16)
play_view = memoryview(play_buffer.tobytes())
sum_buffer = play_buffer.copy()
tock = time.ticks_us()
print(f"computed the samples in {tock-tick} microseconds")


potentiometer = ADC(Pin(26))
keys = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(12)]


async def continuous_loop(audio_out, mv):
    swriter = asyncio.StreamWriter(audio_out)
    while True:
        swriter.write(mv)
        await swriter.drain()
        
async def main(audio_out, sum_buffer):
    play = asyncio.create_task(continuous_loop(audio_out, play_view))
    while True:
        sum_buffer[:] = 0
        amplitude = potentiometer.read_u16() / 2
        for key, filename in zip(keys, filenames):
            if not key.value():
                sum_buffer += np.asarray(amplitude * np.load(filename), dtype=np.int16)
        
        play_buffer[:] = sum_buffer
        await asyncio.sleep(0)



try:
    audio_out = I2S(
        0,
        sck=Pin(18),
        ws=Pin(19),
        sd=Pin(20),
        mode=I2S.TX,
        bits=16,
        format=I2S.MONO,
        rate=22_050,
        ibuf=2* num_samples * 2 #bytes/sample,
    )
    asyncio.run(main(audio_out, sum_buffer))
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))
finally:
    audio_out.deinit()
    print("Done")
