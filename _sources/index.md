# About This Course
## The Data Science Labs on Fourier Analysis
**Alden Bradford and Mireille Boutin**

Welcome to The Data Science Labs on Fourier Analysis! This is a one credit course to accompany ECE301, AAE301 and MA428. In this course, you will explore applications of Fourier analysis concepts (esp. Fourier series) to problems in data science. You will also practice programming in Python and using Arduino sensors and microprocessors. 

This course requires no work outside of the lab, including no homework, no quizzes, no tests, and no exams. All work is performed during the 150 minutes spent in the lab each week. A course on Fourier analysis (either ECE301, AAE301 or MA428) is a co-requisite for taking this course. Some experience in Python is also required (e.g. MA16290)

The material builds on the concept of continuous-time Fourier series to synthesize and analyze signals. A direct connection is made between the continuous-time Fourier series and the discrete fourier transform (DFT), so that no knowledge of the Fourier transform (either continuous-time or discrete-time) is required. 

We are still polishing the last details of the course. The planned first offering is in the Spring semester of 2023. 

<br>

## More Information and Contact

For more information regarding this and the other available Data Science Labs, visit the following link: 
https://engineering.purdue.edu/~mboutin/Data_Science_labs.html

Contact Professor Boutin at mboutin@purdue.edu if you have any more questions regarding this course.
<br>

## How to Get Started

You are reading an interactive Notebook written in the Jupyter language. Jupyter allows for a collection of files to be neatly compiled into a single web-page, such as the one you're looking at. It also allows you to write and compile Python code. 

The application that is used to make these Notebooks is JupyterLab, which is what you'll be using to interact with and edit the labs. 

To get started with this course, click the next arrow at the bottom left of this page to get to Laboratory 1. This lab will explain how to interact with the Notebook, including running code, editing cells, and other useful features that can be used in Jupyter. Throughout the lab, you will be asked to perform some exercises. You will write your answers directly in the Notebook. In other words, you will need to edit the lab file. In order to edit the lab, we recommend downloading the file and opening it in JupyterLab.

To begin editing this lab, click on the download icon in the top right of the screen and download the *.ipynb* version of Lab 0. After this, open the JupyterLab application. This will bring you to a screen with files and a Table of Contents on the left side and a screen on the right side. If not already open, open the files directory by clicking on the folder icon in the top left corner. Open the *Downloads* file, double-click *lab_0.ipynb*, and follow the directions in this lab to begin.

To turn in the labs on Brightspace, you will have to export the file as a PDF. To do this, navigate to *File*, *Save and Export Notebook as*, and then click on *PDF*. This will be further explained in Laboratory 0.

If you have any questions or are experiencing any difficulties during these labs, please ask your TA for assistance.





















Part 1: SYNTHESIZING


What is the meaning of Fourier series coefficients?
1-3: Play a pure cosine wave. Play the scale. Play a song. Observe that playing song twice as fast is faster AND higher pitch. (Fourier series properties) Play a sum of sine and cosine waves with different coefficients. (What are the FS coefficients of sound you create).  Create your own sound (an entire scale). Play a song.

Projects: make a piano, make an instrument where frequency of sound is controlled by ultrasonic distance sensor


4: record voice, scale time to create higher pitch; play a song.

Arduino: modify your piano to use your voice??


5-6: Amplitude modulation: tremolo effect (low frequency modulation) ring effect (modulation with high frequency signal), modulation with triangular wave? Other waves?

Project: voice tremolo effect or more general voice modifier (e.g. https://www.instructables.com/Dalek-Voice-Changer-Arduino-Shield/) 



(Beats: add two cosine waves with close frequency (tuning), write as product (see it’s a modulation)) 



Part 2: ANALYZING


7-9 DFT 


projects: Instrument tuning, Step frequency analysis (compare with thresholding to find steps)

10 Filtering 

projects: remove low-frequency (fan?) noise???