#!/usr/bin/python3

import datetime
import gpiozero
import os
import random
import time
import subprocess
import sys

# Notes
# Set volume: sudo amixer cset numid=1 70%

os.system("killall -9 raspistill")
pir = gpiozero.MotionSensor(pin=4, queue_len=100, sample_rate=100, threshold=.95)
camera = subprocess.Popen(["raspistill", "-s", "-o", "/home/pi/halloweendalek/tmp.jpg"])
lastmovement = datetime.datetime.now()
silenceoriginalweight = 5

responses = []
weights = []

class response:
    def __init__(self, soundfile = None, printstatement = "", weight = 1):
        self.soundfile = soundfile
        self.printstatement = printstatement
        self.weight = weight

    def respond(self):
        print(self.printstatement)
        sys.stdout.flush()
        if self.soundfile:
            os.system("mpg123 -q " + self.soundfile)
            os.kill(camera.pid, 10)
            time.sleep(5)
            os.rename("/home/pi/halloweendalek/tmp.jpg", "/home/pi/halloweendalek/" + str(datetime.datetime.now()).replace(" ", "_") + ".jpg")
            
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
    weight = silenceoriginalweight)

responses.append(silence)
weights.append(silence.weight)

trick = response(\
    soundfile = "/home/pi/halloweendalek/trick-or-treat.mp3", \
    printstatement = "Trick or Treat", \
    weight = .1)

responses.append(trick)
weights.append(trick.weight)


while True:
    if datetime.datetime.now().hour >= 21 or datetime.datetime.now().hour < 9:
        time.sleep(60*60)
    else:
        print("Waiting for motion...")
        sys.stdout.flush()
        pir.wait_for_motion()
        print(datetime.datetime.now())
        sys.stdout.flush()
        reaction = random.choices(responses, weights)
        reaction[0].respond()

        if (datetime.datetime.now() - lastmovement).seconds < 40:
            silence.weight += 2
        elif (datetime.datetime.now() - lastmovement).seconds < 120:
            silence.weight += 1
        elif (datetime.datetime.now() - lastmovement).seconds > 600:
            silence.weight = silenceoriginalweight
        
        if silence.weight > 20 * exterminate.weight:
            silence.weight = 20 * exterminate.weight
        
        
        print("Sleeping...")
        sys.stdout.flush()
        time.sleep(25)
        print("Done sleeping.")
        sys.stdout.flush()
        
        print("Waiting for motion to stop...")
        sys.stdout.flush()
        pir.wait_for_no_motion()
