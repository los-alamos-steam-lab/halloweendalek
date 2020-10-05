#!/usr/bin/python3

import datetime
import gpiozero
#from gpiozero import Button
import os
import random
import time
import subprocess

# Notes
# Set volume: sudo amixer cset numid=1 70%

pir = gpiozero.MotionSensor(pin=4, queue_len=500, sample_rate=100, threshold=0.90)

responses = []
weights = []

class response:
    def __init__(self, soundfile = None, printstatement = "", weight = 1):
        self.soundfile = soundfile
        self.printstatement = printstatement
        self.weight = weight

    def respond(self):
        print(self.printstatement)
        if self.soundfile:
            subprocess.Popen(["raspistill", "-o", "/home/pi/halloweendalek/" + str(datetime.datetime.now()).replace(" ", "_") + ".jpg"])
            time.sleep(4.5)
            os.system("mpg123 -q " + self.soundfile)
 
exterminate = response(\
    soundfile = "/home/pi/halloweendalek/s1_06_aud_03.mp3", \
    printstatement = "EXTERMINATE", \
    weight = 10)

responses.append(exterminate)
weights.append(exterminate.weight)

aghhhh = response(\
    soundfile = "/home/pi/halloweendalek/s1_06_aud_02.mp3", \
    printstatement = "AGHHHH", \
    weight = 1)

responses.append(aghhhh)
weights.append(aghhhh.weight)

silence = response(\
    printstatement = "SILENTLY BIDING MY TIME", \
    weight = 0)

responses.append(silence)
weights.append(silence.weight)

trick = response(\
    soundfile = "/home/pi/halloweendalek/trick-or-treat.mp3", \
    printstatement = "Trick or Treat", \
    weight = .1)

responses.append(trick)
weights.append(trick.weight)


while True:
    print("Waiting for motion...")
    pir.wait_for_motion()
    print(datetime.datetime.now())
    reaction = random.choices(responses, weights)
    reaction[0].respond()
    
    print("Sleeping...")
    time.sleep(10)
    print("Done sleeping.")
    
    print("Waiting for motion to stop...")
    pir.wait_for_no_motion()
