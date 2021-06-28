from gpiozero import Button, AngularServo ,Servo
import RPi.GPIO as GPIO
from time import sleep

motorPin1 = 17
motorPin2 = 27
motorSpeedControl = 4
button = Button(2)
servo = Servo(22)

GPIO.setmode(GPIO.BCM)
GPIO.setup(motorPin1, GPIO.OUT)
GPIO.setup(motorPin2, GPIO.OUT)
GPIO.setup(motorSpeedControl, GPIO.OUT)

p = GPIO.PWM(4, 1000)
P.start(50)

motorMode = 0

def buttonispressed():
    if button.is_pressed:
        sleep(1)
        return 1
    else:
        return 0

while True:
    if motorMode == 3:
        motorMode = 0
    if buttonispressed() == 1:
        print("Button is pressed")
        motorMode += 1
    if motorMode == 0:
        GPIO.output(motorPin1, 0)
        GPIO.output(motorPin2, 0)
        servo.mid()
    elif motorMode == 1:
        GPIO.output(motorPin1, 1)
        GPIO.output(motorPin2, 0)
        servo.max()
    elif motorMode == 2:
        GPIO.output(motorPin1, 0)
        GPIO.output(motorPin2, 1)
        servo.min()

GPIO.cleanup()