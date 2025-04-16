#!/usr/bin/env python

"""tuner.py: A basic implementation of an instrument tuner"""

__author__      = "Mo Chen"

import sounddevice as sd
import numpy as np
from time import sleep


class Tuner():
    def __init__(self):
        self.RATE = 44100       # Sample rate
        self.RECORD_SECONDS = 2 # Duration of recording
        self.CHANNELS = 1       # Mono audio

        self.program_info()

    def program_info(self):
        print('*' * 80)
        info = [
            "This is a simple program used for tuning an instrument.\n",
            "Usage:",
            "Play a note on seeing a prompt.",
            "The program will analyze the note played and display the frequency of the note.",
            "Follow the prompts to redo the tuning or to exit the program"
        ]
        for line in info:
            print(line)
        print('*' * 80)

    def show_menu(self):
        print("\n")
        print("Press 'c' to continue tuning.")
        print("Press 'q' to quit. ")

    def get_recorded_frames(self):
        print("Recording...")
        frames = sd.rec(int(self.RATE * self.RECORD_SECONDS), samplerate=self.RATE, channels=self.CHANNELS, dtype='float32')
        sd.wait()  # Wait until recording is finished
        return frames.flatten()

    def find_max_freq(self, frames):
        fft = np.fft.fft(frames)
        xf = np.fft.fftfreq(len(frames), 1 / self.RATE)
        mag = np.abs(fft)
        idx = np.argmax(mag)
        freq = xf[idx]
        return np.abs(freq)

    def tune(self):
        user_input = ''

        while user_input.lower() != 'q':
            print("Tuner starts in 3 seconds! Get ready to play the note.")
            for i in range(3, 0, -1):
                print(i, end='\r')
                sleep(1)

            print("*************************************")
            print("*******    tuning started!    *******")

            frames = self.get_recorded_frames()
            freq = self.find_max_freq(frames)

            print("*************************************")
            print("Frequency: ", freq)
            print("*************************************")

            self.show_menu()
            user_input = input("Enter your choice: ")

        print("*******    tuning stopped!    *******")
        print("*************************************")


# Run the tuner
tuner = Tuner()
tuner.tune()
