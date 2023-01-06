
import uos
import os
from machine import Pin
from machine import I2S
from sdcard import SDCard
from machine import SPI
import uasyncio
import time;


print("about to start")
if os.uname().machine.count("Raspberry"):
    print("started")
    

    cs = Pin(13, machine.Pin.OUT)
    spi = SPI(
        1,
        baudrate=1000000,  # this has no effect on spi bus speed to SD Card
        polarity=0,
        phase=0,
        bits=8,
        firstbit=machine.SPI.MSB,
        sck=Pin(14),
        mosi=Pin(15),
        miso=Pin(12),
    )
    
    
    sd = SDCard(spi, cs)
    sd.init_spi(1000000)  # increase SPI bus speed to SD card
    print("about to mount sd card")
    
    vfs = uos.VfsFat(sd)
    uos.mount(vfs, "/sd")
    
    print("sd card mounted")


    # ======= I2S CONFIGURATION =======
    SCK_PIN = 16
    WS_PIN = 17
    SD_PIN = 18
    I2S_ID = 0
    BUFFER_LENGTH_IN_BYTES = 60000  # larger buffer to accommodate slow SD card driver
    # ======= I2S CONFIGURATION =======


else:
    print("Warning: program not tested with this board")

# ======= AUDIO CONFIGURATION =======
WAV_FILE = "recording4.wav"
RECORD_TIME_IN_SECONDS = 5
WAV_SAMPLE_SIZE_IN_BITS = 16
FORMAT = I2S.MONO
SAMPLE_RATE_IN_HZ = 22050
# ======= AUDIO CONFIGURATION =======
print("crossed configs")


NUM_CHANNELS = 1
WAV_SAMPLE_SIZE_IN_BYTES = WAV_SAMPLE_SIZE_IN_BITS // 8
RECORDING_SIZE_IN_BYTES = (
    RECORD_TIME_IN_SECONDS * SAMPLE_RATE_IN_HZ * WAV_SAMPLE_SIZE_IN_BYTES * NUM_CHANNELS
)


def create_wav_header(sampleRate, bitsPerSample, num_channels, num_samples):
    print("created wav header")
    datasize = num_samples * num_channels * bitsPerSample // 8
    
    print("data size: "+ str(datasize))
    o = bytes("RIFF", "ascii")  # (4byte) Marks file as RIFF
    o += (datasize + 36).to_bytes(
        4, "little"
    )  # (4byte) File size in bytes excluding this and RIFF marker
    o += bytes("WAVE", "ascii")  # (4byte) File type
    o += bytes("fmt ", "ascii")  # (4byte) Format Chunk Marker
    o += (16).to_bytes(4, "little")  # (4byte) Length of above format data
    o += (1).to_bytes(2, "little")  # (2byte) Format type (1 - PCM)
    o += (num_channels).to_bytes(2, "little")  # (2byte)
    o += (sampleRate).to_bytes(4, "little")  # (4byte)
    o += (sampleRate * num_channels * bitsPerSample // 8).to_bytes(4, "little")  # (4byte)
    o += (num_channels * bitsPerSample // 8).to_bytes(2, "little")  # (2byte)
    o += (bitsPerSample).to_bytes(2, "little")  # (2byte)
    o += bytes("data", "ascii")  # (4byte) Data Chunk Marker
    o += (datasize).to_bytes(4, "little")  # (4byte) Data size in bytes
    print("created wav header")
    return o


wav = open("/sd/{}".format(WAV_FILE), "ab")

# create header for WAV file and write to SD card
wav_header = create_wav_header(
    SAMPLE_RATE_IN_HZ,
    WAV_SAMPLE_SIZE_IN_BITS,
    NUM_CHANNELS,
    SAMPLE_RATE_IN_HZ * RECORD_TIME_IN_SECONDS,
)


num_bytes_written = wav.write(wav_header)

audio_in = I2S(
    I2S_ID,
    sck=Pin(SCK_PIN),
    ws=Pin(WS_PIN),
    sd=Pin(SD_PIN),
    mode=I2S.RX,
    bits=WAV_SAMPLE_SIZE_IN_BITS,
    format=FORMAT,
    rate=SAMPLE_RATE_IN_HZ,
    ibuf=BUFFER_LENGTH_IN_BYTES,
)

# allocate sample arrays
# memoryview used to reduce heap allocation in while loop
mic_samples = bytearray(10000)
mic_samples_mv = memoryview(mic_samples)

num_sample_bytes_written_to_wav = 0

print("Recording size: {} bytes".format(RECORDING_SIZE_IN_BYTES))
print("==========  START RECORDING ==========")
try:
    while num_sample_bytes_written_to_wav < RECORDING_SIZE_IN_BYTES:
        # read a block of samples from the I2S microphone
        num_bytes_read_from_mic = audio_in.readinto(mic_samples_mv)
        
        if num_bytes_read_from_mic > 0:
            num_bytes_to_write = min(
                num_bytes_read_from_mic, RECORDING_SIZE_IN_BYTES - num_sample_bytes_written_to_wav
            )
            print("writing")
            # write samples to WAV file
            num_bytes_written = wav.write(mic_samples_mv[:num_bytes_to_write])
            

            time.sleep(0.001)
            print("-----------------------------")
            num_sample_bytes_written_to_wav += num_bytes_written
            
    print("==========  DONE RECORDING ==========")
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))
    

wav.close();

if os.uname().machine.count("Raspberry"):
    os.umount("/sd")
    spi.deinit()
    
audio_in.deinit()