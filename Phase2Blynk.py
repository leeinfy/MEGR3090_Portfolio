import RPi.GPIO as GPIO
import blynklib
import time
import random

#blynk Author code
BLYNK_AUTH = 'B8ltEMSYdnD9pn0rWOC_vC4oXMNBDecF'

# initialize blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

joystick_x_position = 128
joystick_y_position = 128

state = 0

# register handler for virtual pin V0 write event
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global state
    if value == 0:
        state = 0
    elif value == 1:
        state = 1

# register handler for virtual pin V0 write event
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global joystick_x_position
    joystick_x_position = value

# register handler for virtual pin V0 write event
@blynk.handle_event('write V2')
def write_virtual_pin_handler(pin, value):
    value = int(format(value[0]))
    global joystick_y_position
    joystick_y_position = value
       
while True:
    blynk.run()
