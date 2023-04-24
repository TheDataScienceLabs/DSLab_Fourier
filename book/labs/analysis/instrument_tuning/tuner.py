#!/usr/bin/env python

"""tuner.py: A basic implementation of an instrument tuner"""

__author__      = "Adharsh Sabukumar"



import pyaudio
import wave
import numpy as np

from time import sleep



class Tuner():
    def __init__(self):
        self.chunk = 1000
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 2
        self.swidth = 2

        self.program_info()


    def open_stream_for_tuning(self):
        
        p = pyaudio.PyAudio()

        stream = p.open(format = self.FORMAT,
                    channels = self.CHANNELS,
                    rate = self.RATE,
                    input = True,
                    frames_per_buffer = self.chunk)

        return p, stream

    def close_audio_stream(self, p, stream):

        stream.stop_stream()
        stream.close()
        p.terminate()


    def program_info(self):

        print('*'*80)

        info = ["This is a simple program used for tuning an instrument.", "\n","Usage:", "Play a note on seeing a prompt."]
        info.append("The program will analyze the note played and display the frequency of the note.")
        info.append("Follow the promts to redo the tuning or to exit the program")

        for line in info:
            print(line)

        print('*'*80)

    def show_menu(self):

        info = ["\n"]
        info.append("Press 'c' to continue tuning.")
        info.append("Press 'q' to quit. ")


        for msg in info:
            print(msg)


    def get_recorded_frames(self, stream):

        frames = list()

        for i in range(0, self.RATE//self.chunk * self.RECORD_SECONDS):

            data = stream.read(self.chunk, exception_on_overflow = False)
            data_length = len(data)//self.swidth

            frame = wave.struct.unpack("%dh"%(data_length), data)
            frames.extend(list(frame))

        return frames

    def find_max_freq(self, frames):

        fft = np.fft.fft(frames)
        xf = np.fft.fftfreq(len(frames), 1/self.RATE)
        mag = np.abs(fft)
        idx = np.argmax(mag)
        freq = xf[idx]

        return np.abs(freq)

    def tune(self):

        
        user_input = ''

        while user_input != 'q':

            print("Tuner starts in 3 seconds! Get ready to play the note.")

            for i in range(4, 0, -1):
                print(i, end = '\r')
                sleep(1)

            p, stream = self.open_stream_for_tuning()
            print("*************************************")
            print("*******    tuning started!    *******")


            #get recordings as a numpy array
            frames = np.array(self.get_recorded_frames(stream))

            # identify dominant frequency for tuning.
            freq = self.find_max_freq(frames)

            print("*************************************")
            print("Frequency: ", freq)
            print("*************************************")
            self.close_audio_stream(p, stream)

            self.show_menu()
            user_input = input("Enter your choice: ")


            if (user_input == 'q' or user_input == 'Q'):
                break

        print("*******    tuning stopped!    *******")
        print("*************************************")


        self.close_audio_stream(p, stream)


# create an instance of the class
tuner = Tuner()
#call the tune function
tuner.tune()
