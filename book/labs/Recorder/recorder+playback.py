from machine import Pin, I2S
import sdcard
import os, uos
import wave


# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(13, machine.Pin.OUT)

# Intialize SPI peripheral (start with 1 MHz)
spi = machine.SPI(1,
                  baudrate=1000000,
                  polarity=0,
                  phase=0,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(14),
                  mosi=machine.Pin(15),
                  miso=machine.Pin(12))

# Initialize SD card
sd = sdcard.SDCard(spi, cs)
print("SD card initialized")
# Mount filesystem
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")
print("SD card Mounted")


wav =  open("/sd/recording.wav", "rb+");

print("Found wav file")




#initialize the I2S device


i2s = I2S(
    0,
    sck=Pin(0),
    ws=Pin(1),
    sd=Pin(2),
    mode=I2S.TX,
    bits=16,
    format=I2S.MONO,
    rate=22050,
    ibuf=2000,
)

print("I2S object created")


#create a function to play the wav
def wav_player(fname):
    wav = wave.open(fname)

    while True:
        print("playing")
        data = wav.readframes(102)
        if len(data) > 0:
            i2s.write(data)
        else:
            wav.close()
            break


print("about to play audio")

wav_player('/sd/recording2.wav')
#point the directory to the files you have on your sd card - works best with short low file size wavs

i2s.deinit()
spi.deinit()

print("Done playing")
