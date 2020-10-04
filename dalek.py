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

while True:
    print("Waiting for motion...")
    pir.wait_for_motion()
    print(datetime.datetime.now())
    randnum = random.randrange(10)
    if randnum == 1:
        print("AGHHHH")
#        os.system("mpg123 -q /home/pi/halloweendalek/s1_06_aud_02.mp3")
    elif randnum in [0, 2, 4, 6, 8]:
        print("EXTERMINATE")
#        os.system("mpg123 -q /home/pi/halloweendalek/s1_06_aud_03.mp3")
    else:
        print("SILENTLY BIDING MY TIME")
    #print("Sleeping...")
    #time.sleep(10)
    #print("Done sleeping.")
    print("Waiting for motion to stop...")
    pir.wait_for_no_motion()
