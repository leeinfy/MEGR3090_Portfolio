import RPi.GPIO as GPIO
import blynklib
import time

#blynk Author code
BLYNK_AUTH = 'B8ltEMSYdnD9pn0rWOC_vC4oXMNBDecF'

# initialize blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

joystick_x_position = 128
joystick_y_position = 128
state = 0
left_motor_speed = 0
right_motor_speed = 0
GPIO.setmode(GPIO.BCM)

horizontal_servo = 2
GPIO.setup(horizontal_servo, GPIO.OUT)
horizontalServoPWM =  GPIO.PWM(horizontal_servo,50)
horizontalServoPWM.start(0)

# register handler for virtual pin V0 write event
@blynk.handle_event('write V0')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global joystick_x_position
    joystick_x_position = value

# register handler for virtual pin V0 write event
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global joystick_y_position
    joystick_y_position = value

# register handler for horizontal slider of camera servo
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    slidervalue = float(format(value[0]))
    horizontalServoPWM.ChangeDutyCycle(SliderNumberToServoDutyCycle(slidervalue))
    time.sleep(.3)
    horizontalServoPWM.ChangeDutyCycle(0)

# slider value to duty cycle convert equation
def SliderNumberToServoDutyCycle(value):
    return 3 + value

       
while True:
    blynk.run()
