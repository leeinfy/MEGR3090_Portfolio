import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo = 2
GPIO.setup(servo,GPIO.OUT)
p =  GPIO.PWM(servo,50) #Setup PWM with 50HZ
p.start(0)
#play with the number X in p.ChangeDutyCycle(X) to change the direction of servo
#In this case my high band width is 1.5ms
#for band width length check the datasheet
#My servo is Micro Servo 9g S51, and my range is from 2 to 13
#change frequency with code p.Changefrequency(X)
while True:
    a = float(input())
    p.ChangeDutyCycle(a)
    time.sleep(.3)
    p.ChangeDutyCycle(0)


    
    