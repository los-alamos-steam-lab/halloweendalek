#!/usr/bin/python3

import datetime
import gpiozero
#from gpiozero import Button
import os
import random
import time

# Notes
# Set volume: sudo amixer cset numid=1 70%

#button = Button(4, pull_up=False, bounce_time=60)
#
#while True:
#    button.wait_for_press()
#    print("EXTERMINATE")
#    os.system("mpg123 /home/pi/halloweendalek/s1_06_aud_03.mp3")
#    button.wait_for_release()

pir = gpiozero.MotionSensor(pin=4, queue_len=500, sample_rate=100, threshold=0.90)

responses = []
weights = []

class response:
    def __init__(self, soundfile = None, printstatement = "", weight = 10):
        self.soundfile = soundfile
        self.printstatement = printstatement
        self.weight = weight

    def respond(self):
        print(self.printstatement)
        if self.soundfile:
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
    weight = 10)

responses.append(aghhhh)
weights.append(aghhhh.weight)

silence = response(\
    printstatement = "SILENTLY BIDING MY TIME", \
    weight = 10)

responses.append(silence)
weights.append(silence.weight)


while True:
    print("Waiting for motion...")
    pir.wait_for_motion()
    print(datetime.datetime.now())
    reaction = random.choices(responses, weights)
    reaction[0].respond()
    #print("Sleeping...")
    #time.sleep(10)
    #print("Done sleeping.")
    print("Waiting for motion to stop...")
    pir.wait_for_no_motion()
