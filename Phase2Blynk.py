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
left_motor_pin1 = 10
left_motor_pin2 = 9
left_motor_speed_pin = 11
GPIO.setup(left_motor_pin1, GPIO.OUT)
GPIO.setup(left_motor_pin2, GPIO.OUT)
GPIO.setup(left_motor_speed_pin, GPIO.OUT)
leftMotorPWM = GPIO.PWM(left_motor_speed_pin, 100)
leftMotorPWM.start(0)

#right motor initialize
right_motor_pin1 = 17
right_motor_pin2 = 27
right_motor_speed_pin = 22
GPIO.setup(right_motor_pin1, GPIO.OUT)
GPIO.setup(right_motor_pin2, GPIO.OUT)
GPIO.setup(right_motor_speed_pin, GPIO.OUT)
rightMotorPWM = GPIO.PWM(left_motor_speed_pin, 100)
rightMotorPWM.start(0)

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
    
# register V1 write for joystick y value
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global joystick_Y_position
    joystick_Y_position = value

# register V2 write for horizontal slider of camera servo
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    slidervalue = float(format(value[0]))
    horizontalServoPWM.ChangeDutyCycle(SliderNumberToServoDutyCycle(3+value)) #slider value is from 0 to 10 and the servo duty cycle is from 3 to 13
    time.sleep(.3)
    horizontalServoPWM.ChangeDutyCycle(0)
     
# left motor  movement
def leftMotorRun(xValue, yValue):
    #motor in driving mode
    if yValue >= 155:  #left motor go forward
        GPIO.output(left_motor_pin1,0)
        GPIO.output(left_motor_pin2,1)
        if xValue >100:
            leftMotorPWM.ChangeDutyCycle(yValue-155)  #left motor speed increase from y 155 to 155
        elif xValue <=100:
            leftMotorPWM.ChangeDutyCycle ((yValue-155)/100 * xValue)# left motor speed increase form x 0 to 100
    elif yValue <= 100:  #left motor go backward
        GPIO.output(left_motor_pin1,1)
        GPIO.output(left_motor_pin2,0)
        if xValue < 155:
            leftMotorPWM.ChangeDutyCycle(100- yValue)  #left motor speed decrease from y 0 to 100
        elif xValue >=155:
            leftMotorPWM.ChangeDutyCycle ((100 - yValue)/100*(255-yValue))# left motor speed decrease from x 155 to 255
    #motor in pivot mode
    elif 100 < yValue < 155:
        if xValue <= 100: #leftmotor go backward
            GPIO.output(left_motor_pin1,1)
            GPIO.output(left_motor_pin2,0)
            leftMotorPWM.ChangeDutyCycle(100- xValue) #left motor speed decrease from 0 to 100 
        elif xValue >= 155: #leftmotor go forward
            GPIO.output(left_motor_pin1,0)
            GPIO.output(left_motor_pin2,1)
            leftMotorPWM.ChangeDutyCycle(xValue-155) #left motor speed increase from 155 to 255
        #motor is stop
        elif 100< xValue <155:
            GPIO.output(left_motor_pin1,0)
            GPIO.output(left_motor_pin2,0)
            leftMotorPWM.ChangeDutyCycle(0)

# right motor  movement
def rightMotorRun(xValue, yValue):
    #motor in driving mode
    if yValue >= 155:  #right right go forward
        GPIO.output(right_motor_pin1,0)
        GPIO.output(right_motor_pin2,1)
        if xValue >=155:
            rightMotorPWM.ChangeDutyCycle((255 - yValue)/100*(255-yValue))  #right motor speed decrease from x 155 to 255
        elif xValue < 155:
            rightMotorPWM.ChangeDutyCycle (yValue-155)# right motor speed increase form y 155 to 255
    elif yValue <= 100:  #right motor go backward
        GPIO.output(right_motor_pin1,1)
        GPIO.output(right_motor_pin2,0)
        if xValue <= 100:
            rightMotorPWM.ChangeDutyCycle((100- yValue)/100*xValue)  #right motor speed increase from x 0 to 100
        elif xValue > 100:
            rightMotorPWM.ChangeDutyCycle (100 - yValue)# right motor speed decrease from y 0 to 100
    #motor in pivot mode
    elif 100 < yValue < 155:
        if xValue <= 100: #right motor go forward
            GPIO.output(right_motor_pin1,1)
            GPIO.output(right_motor_pin2,0)
            rightMotorPWM.ChangeDutyCycle(100- xValue) #rihgt motor speed decrease from 0 to 100 
        elif xValue >= 155: #leftmotor go backward
            GPIO.output(right_motor_pin1,0)
            GPIO.output(right_motor_pin2,1)
            rightMotorPWM.ChangeDutyCycle(xValue-155) #right motor speed increase from 155 to 255
        #motor is stop
        elif 100< xValue <155:
            GPIO.output(right_motor_pin1,0)
            GPIO.output(right_motor_pin2,0)
            rightMotorPWM.ChangeDutyCycle(0)
                  
while True:
    blynk.run()
    leftMotorRun(joystick_X_position, joystick_Y_position)
    rightMotorRun(joystick_X_position, joystick_Y_position)
    
