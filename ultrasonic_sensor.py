import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
#set GPIO Pins
SENSOR_TRIGGER = 18
SENSOR_ECHO = 24

LED_PIN = 12
 
#set GPIO direction (IN / OUT)
GPIO.setup(SENSOR_TRIGGER, GPIO.OUT)
GPIO.setup(SENSOR_ECHO, GPIO.IN)

GPIO.setup(LED_PIN, GPIO.OUT)  # Set GPIO pin 12 to output mode.
pwm = GPIO.PWM(LED_PIN, 100)   # Initialize PWM on pwmPin 100Hz frequency

# Ensure first reading is clean
GPIO.output(SENSOR_TRIGGER, GPIO.LOW)

# Set duty cycle variable to 0 for 0%
dc=0
pwm.start(dc)
 
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
        if dist > 50:
            dc = 0
        else:
            dc = 100 - 2*dist
        pwm.ChangeDutyCycle(dc)
        time.sleep(1)
    # Reset by pressing CTRL + C
except KeyboardInterrupt:
    print("Measurement stopped by User")
    pwm.stop()
    GPIO.cleanup()