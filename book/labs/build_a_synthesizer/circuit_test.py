"""
This code plays a simple tone to a connected I2S speaker
for one second, just to see if everything is working.
"""
import time
from machine import I2S, Pin

tone = b'\x00\x00\x05\x08\xea\x0f\x8f\x17\xd5\x1e\x9e%\xcf+P1\t6\xe89\xde<\xdd>\xdf?\xdf?\xdd>\xde<\xe89\t6P1\xcf+\x9e%\xd5\x1e\x8f\x17\xea\x0f\x05\x08\x00\x00\xfb\xf7\x16\xf0q\xe8+\xe1b\xda1\xd4\xb0\xce\xf7\xc9\x18\xc6"\xc3#\xc1!\xc0!\xc0#\xc1"\xc3\x18\xc6\xf7\xc9\xb0\xce1\xd4b\xda+\xe1q\xe8\x16\xf0\xfb\xf7'

try:
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

    starttime = time.ticks_ms()
    while time.ticks_ms() < starttime + 2000:
        audio_out.write(tone)
finally:
    audio_out.deinit()
