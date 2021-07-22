import RPi.GPIO as GPIO
import blynklib
import time

#blynk Author code
BLYNK_AUTH = 'B8ltEMSYdnD9pn0rWOC_vC4oXMNBDecF'

# initialize blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

#disable warning
GPIO.setwarnings(False)

#raspberry GPIO configeration
GPIO.setmode(GPIO.BCM)

#left motor initialize
left_motor_pin1 = 17
left_motor_pin2 = 27
left_motor_speed_pin = 22
GPIO.setup(left_motor_pin1, GPIO.OUT)
GPIO.setup(left_motor_pin2, GPIO.OUT)
GPIO.setup(left_motor_speed_pin, GPIO.OUT)
leftMotorPWM = GPIO.PWM(left_motor_speed_pin, 100)
leftMotorPWM.start(0)

#horizontal movement servo of camera mount initialize
horizontal_servo = 2
GPIO.setup(horizontal_servo, GPIO.OUT)
horizontalServoPWM =  GPIO.PWM(horizontal_servo,50)
horizontalServoPWM.start(0)

#global variable
joystick_X_position = 128
joystick_Y_position = 128

# register V0 write for joystick X value
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global joystick_X_position
    joystick_X_position = value
    
# register handler for virtual pin V0 write event
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global joystick_Y_position
    joystick_Y_position = value

# register V2 write for horizontal slider of camera servo
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    slidervalue = float(format(value[0]))
    horizontalServoPWM.ChangeDutyCycle(SliderNumberToServoDutyCycle(slidervalue))
    time.sleep(.3)
    horizontalServoPWM.ChangeDutyCycle(0)

# slider value to duty cycle convert equation
def SliderNumberToServoDutyCycle(value):
    #slider value is from 0 to 10 and the servo duty cycle is from 3 to 13
    # duty cycle 7.5, and slider value 4.5 is middle point
    return 3 + value   

# left Motor state base on the joystick position
def leftMotorRun(xValue, yValue):
    if 100< xValue <155: #joystick X is in the middle
        if 0 <= yValue <= 100: #joystick y is upward motor go forward
            GPIO.output(left_motor_pin1, 0)
            GPIO.output(left_motor_pin2, 1)
            leftMotorPWM.ChangeDutyCycle(JoystickNumberToMotorDutyCycle(yValue))
        elif 100< yValue <155: #joystick y is in the middle motor stop
            GPIO.output(left_motor_pin1, 0)
            GPIO.output(left_motor_pin2, 0)
            leftMotorPWM.ChangeDutyCycle(0)
        elif 155 <= yValue <=255: #joystick y is downward motor go downward
            GPIO.output(left_motor_pin1, 1)
            GPIO.output(left_motor_pin2, 0)
            leftMotorPWM.ChangeDutyCycle(JoystickNumberToMotorDutyCycle(yValue))
        
def JoystickNumberToMotorDutyCycle(value):
    if value >= 155:
        dutycycle = value - 155
    elif value <= 100:
        dutycycle = 100 -value
    return dutycycle
        
                     
while True:
    blynk.run()
    leftMotorRun(joystick_X_position, joystick_Y_position)
    
