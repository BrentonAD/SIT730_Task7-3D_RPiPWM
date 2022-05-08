import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
SENSOR_TRIGGER = 18
SENSOR_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(SENSOR_TRIGGER, GPIO.OUT)
GPIO.setup(SENSOR_ECHO, GPIO.IN)

# Ensure first reading is clean
GPIO.output(SENSOR_TRIGGER, GPIO.LOW)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(SENSOR_TRIGGER, GPIO.HIGH)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(SENSOR_TRIGGER, GPIO.LOW)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(SENSOR_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(SENSOR_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
try:
    while True:
        dist = distance()
        print ("Measured Distance = %.1f cm" % dist)
        time.sleep(1)
 
    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()