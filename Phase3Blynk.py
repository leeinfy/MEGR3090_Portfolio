import RPi.GPIO as GPIO
import blynklib
import pigpio
import array as arr
from time import sleep
from gpiozero import DistanceSensor

#blynk Author code
BLYNK_AUTH = 'B8ltEMSYdnD9pn0rWOC_vC4oXMNBDecF'

# initialize blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

#disable warning
GPIO.setwarnings(False)

#raspberry GPIO configeration
GPIO.setmode(GPIO.BCM)

#left motor initialize
left_motor_forward_pin = 17
left_motor_backward_pin = 27
left_motor_speed_pin = 22
GPIO.setup(left_motor_backward_pin, GPIO.OUT)
GPIO.setup(left_motor_forward_pin, GPIO.OUT)
GPIO.setup(left_motor_speed_pin, GPIO.OUT)
leftMotorPWM = GPIO.PWM(left_motor_speed_pin, 100)
leftMotorPWM.start(0)

#right motor initialize
right_motor_forward_pin = 14
right_motor_backward_pin = 15
right_motor_speed_pin = 18
GPIO.setup(right_motor_backward_pin, GPIO.OUT)
GPIO.setup(right_motor_forward_pin, GPIO.OUT)
GPIO.setup(right_motor_speed_pin, GPIO.OUT)
rightMotorPWM = GPIO.PWM(right_motor_speed_pin, 100)
rightMotorPWM.start(0)


#unlock pigpio
pi = pigpio.pi()

# servo of ultasonic sensor
servo = 26
pi.set_PWM_frequency(servo, 50)

sensor = DistanceSensor(20,21)

# register V0 write for joystick X value
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    buttonValue = int(format(value[0]))
    if buttonValue == 1:
        GPIO.output(left_motor_forward_pin, 1)
        GPIO.output(left_motor_backward_pin, 0)
        GPIO.output(right_motor_forward_pin, 1)
        GPIO.output(right_motor_backward_pin, 0)
    else:
        GPIO.output(left_motor_forward_pin, 0)
        GPIO.output(left_motor_backward_pin, 0)
        GPIO.output(right_motor_forward_pin, 0)
        GPIO.output(right_motor_backward_pin, 0)
    
# register V1 write for joystick y value
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    buttonValue = int(format(value[0]))
    if buttonValue == 1:
        GPIO.output(left_motor_forward_pin, 0)
        GPIO.output(left_motor_backward_pin, 1)
        GPIO.output(right_motor_forward_pin, 1)
        GPIO.output(right_motor_backward_pin, 0)
    else:
        GPIO.output(left_motor_forward_pin, 0)
        GPIO.output(left_motor_backward_pin, 0)
        GPIO.output(right_motor_forward_pin, 0)
        GPIO.output(right_motor_backward_pin, 0)

# register V2 write for horizontal slider of camera servo
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    buttonValue = int(format(value[0]))
    if buttonValue == 1:
        GPIO.output(left_motor_forward_pin, 1)
        GPIO.output(left_motor_backward_pin, 0)
        GPIO.output(right_motor_forward_pin, 0)
        GPIO.output(right_motor_backward_pin, 1)
    else:
        GPIO.output(left_motor_forward_pin, 0)
        GPIO.output(left_motor_backward_pin, 0)
        GPIO.output(right_motor_forward_pin, 0)
        GPIO.output(right_motor_backward_pin, 0)

@blynk.handle_event('write V3')
def write_virtual_pin_handler(pin, value):
    buttonValue = int(format(value[0]))
    if buttonValue == 1:
        GPIO.output(left_motor_forward_pin, 0)
        GPIO.output(left_motor_backward_pin, 1)
        GPIO.output(right_motor_forward_pin, 0)
        GPIO.output(right_motor_backward_pin, 1)
    else:
        GPIO.output(left_motor_forward_pin, 0)
        GPIO.output(left_motor_backward_pin, 0)
        GPIO.output(right_motor_forward_pin, 0)
        GPIO.output(right_motor_backward_pin, 0)

@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    sliderValue = int(format(value[0]))
    leftMotorPWM.ChangeDutyCycle(sliderValue)
    rightMotorPWM.ChangeDutyCycle(sliderValue)
    
@blynk.handle_event('write V5')
def write_virtual_pin_handler(pin, value):
    buttonValue = int(format(value[0]))
    if buttonValue == 1:
        measuredDistance = arr.array('d', [])
        pi.set_PWM_dutycycle(servo, 8)
        sleep(2)
        for i in range(24):
            pi.set_PWM_dutycycle(servo, 8 + i*.83)
            sleep(.5)
            measuredDistance.append(sensor.distance)
            with open('test.txt', 'a') as f:
                f.write('distance at ' + str(i*15) +' degree: '+str(measuredDistance[i])+'\n')
         
while True:
    blynk.run()

