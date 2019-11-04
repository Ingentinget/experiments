#Libraries
import RPi.GPIO as GPIO
import time
import subprocess
import os
stage = 0

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

#set GPIO Pins
GPIO_TRIGGER = 10
GPIO_ECHO = 18

#variabel
IsPlaying = False

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            print ("Measured Distance = %.1f cm" % dist)
            if dist < 200 and dist > 120:
                if IsPlaying == False:
                    print "start flower"
                    video = subprocess.Popen(["omxplayer", "--loop", "./1.mp4", ])
                    IsPlaying = True
                    time.sleep(5)
            else:
                IsPlaying = False
                time.sleep(5)

            if dist < 90 and dist > 57:
                if IsPlaying == False:
                    print "start seal"
                    video = subprocess.Popen(["omxplayer", "--loop", "./2.mp4", ])
                    IsPlaying = True
                    time.sleep(5)
            else:
                IsPlaying = False
                time.sleep(5)
            if dist < 57 and dist > 10:
                if IsPlaying == False:
                    print "start dog"
                    video = subprocess.Popen(["omxplayer", "--loop", "./3.mp4", ])
                    IsPlaying = True
                    time.sleep(5)
            else:
                IsPlaying = False
                time.sleep(5)

            if IsPlaying == False:
                print "stop"
                os.system('killall omxplayer.bin')
                time.sleep(2)

            time.sleep(1)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
