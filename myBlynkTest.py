import blynklib
import random

BLYNK_AUTH = 'B8ltEMSYdnD9pn0rWOC_vC4oXMNBDecF'

# initialize blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

READ_PRINT_MSG = "[READ_VIRTUAL_PIN_EVENT] Pin: V{}"


# register handler for virtual pin V11 reading
@blynk.handle_event('read V2')
def read_virtual_pin_handler(pin):
    print(READ_PRINT_MSG.format(pin))
    blynk.virtual_write(pin, random.randint(0, 255))


###########################################################
# infinite loop that waits for event
###########################################################
while True:
    blynk.run()