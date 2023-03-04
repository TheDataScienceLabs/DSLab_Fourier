import pyaudio
import wave

filename = 'my_recording.wav'

# Sample size per audio frame
chunk = 1024  

# open audio file
wf = wave.open(filename, 'rb')

p = pyaudio.PyAudio()

# initialize an audio output stream.

stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# read data in chunks
data = wf.readframes(chunk)

print("*************************************")
print("*******   playback started!   *******")

while data != '':
    stream.write(data)
    data = wf.readframes(chunk)

print("*************************************")
print("*******   finished playback   *******")


stream.close()
p.terminate()