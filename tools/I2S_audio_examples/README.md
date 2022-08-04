All these examples share the same wiring, for ease of testing. It goes as follows.

Pico| MAX98357 (speaker)
-|-
GP10| BCLK/SCK
GP11| LRC/WS
GP12| DIN/SD
VBUS| Vin
GND | GND

Pico| SPH0645LM4H
-|-
GP13| BCLK/SCK
GP14| LRCL/WS
GP15| DOUT/SD
3V3 | 3V
GND | GND

In addition:

- there are two buttons pulling GP16 and GP17 to ground.
- There is a potentiometer wiping GP26 between ground and 3V3.

To make the computation go faster (in particular the FFTs) we will use a special version of the Micropython firmware which includes a version of numpy. [We can find the latest version here](https://github.com/v923z/micropython-builder), though the version I tested on is included in this directory as `PICO.uf2`.

