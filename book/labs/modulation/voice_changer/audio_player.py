import pyaudio
import wave

filename = 'my_recording.wav'

# Sample size per audio frame
chunk = 1024  

# open audio file for reading in binary mode
wf = wave.open(filename, 'rb')

p = pyaudio.PyAudio() # Initialize the PyAudio object

# Extract audio format information 
FORMAT = p.get_format_from_width(wf.getsampwidth())  # Set the format based on the sample width
CHANNELS = wf.getnchannels()  # Get the number of channels 
RATE = wf.getframerate()  # Get the sampling rate (samples per second)

# Open an audio stream for playback
stream = p.open(format=FORMAT, 
                channels=CHANNELS,  # Set the number of audio channels
                rate=RATE,  # Set the sampling rate
                output=True)  # Indicate that the stream is for output (playback)

# read data in chunks
data = wf.readframes(chunk)

print("*************************************")
print("*******   playback started!   *******")

while data != b'': # Continue reading and playing back data until the end of the file
    stream.write(data)   # Write the audio data to the stream for playback
    data = wf.readframes(chunk)   # Read the next chunk of audio data
    
print("*************************************")
print("*******   finished playback   *******")

wf.close()  # Close the wave file
stream.close()  # Close the audio stream
p.terminate()  # Terminate the PyAudio session