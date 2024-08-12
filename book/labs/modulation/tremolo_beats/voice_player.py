import pyaudio
import wave

chunk = 1024  # Number of frames to read at a time (chunk size)

# Open the wave file for reading in binary mode
wf = wave.open("my_recording.wav", 'rb')

# Extract audio format information from the wave file
FORMAT = pyaudio.paInt16  # Assuming the audio file uses 16-bit samples
CHANNELS = wf.getnchannels()  # Get the number of channels 
RATE = wf.getframerate()  # Get the sampling rate (samples per second)

# Initialize the PyAudio object
p = pyaudio.PyAudio()

# Open an audio stream for playback
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),  # Set the format based on the sample width
                channels=CHANNELS,  # Set the number of audio channels
                rate=RATE,  # Set the sampling rate
                output=True)  # Indicate that the stream is for output (playback)

# Read and play the audio data in chunks
data = wf.readframes(chunk)  # Read the first chunk of audio data

# Continue reading and playing back data until the end of the file
while data:
    stream.write(data)  # Write the audio data to the stream for playback
    data = wf.readframes(chunk)  # Read the next chunk of audio data


wf.close()  # Close the wave file
stream.close()  # Close the audio stream
p.terminate()  # Terminate the PyAudio session
