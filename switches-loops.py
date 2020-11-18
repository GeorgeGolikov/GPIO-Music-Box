# Numbers of the GPIO Ports connected to the devices on the breadboard below:
# switches - gpios
# 1 - 10
# 2 - 9
# 3 - 11

# buttons - gpios
# 1 - 4
# 2 - 17

# leds - gpios
# 1 - 2
# 2 - 3
# 3 - 23

import pygame # import library for gamification

# import classes for leds, switches and buttons to be connected with the script
from gpiozero import Button, LED

pygame.init()

FILE_TO_SHARE_PATH = "./file_to_share.txt"
NUM_LEDS_SWITCHES = 3

# lists of LED and Button objects representing physical devices. Arg of the constructor - number of the gpio port
leds = [LED(2), LED(3), LED(23)]
switches = [Button(10), Button(9), Button(11)]
buttons = [Button(4), Button(17)]
leds_for_buts = [LED(24), LED(25)]

# loop to map the values of switches to the values of leds on the start of this program
# switch pressed - led on, switch released - led off
for i in range(NUM_LEDS_SWITCHES):
    leds[i].value = switches[i].value

# function to change audio effect when a switch is pressed
# takes the object of the switch as an argument
def change_effect(device):
    pin_num = device.pin.number # gpio pin number
    file = open(FILE_TO_SHARE_PATH, 'r+')
    if pin_num == 10:
        file.seek(0)
        leds[0].toggle() # change the state of the 1st led
    if pin_num == 9:        
        file.seek(2)
        leds[1].toggle() # change the state of the 2nd led
    if pin_num == 11:
        file.seek(4)
        leds[2].toggle() # change the state of the 3rd led
    file.write(str(int(device.is_pressed)))
    file.close()
    
# function to change the length of echo when a button is clicked 
# takes the object of the button as an argument
def change_volume(device):
    pin_num = device.pin.number
    file = open(FILE_TO_SHARE_PATH, 'r+')
    file.seek(6)
    val = int(file.read())
    file.seek(6)
    print(val)
    if pin_num == 4:
        if 0 < val < 8:
            file.write(str(val+1))
            # the led blinks 1 time when you click the button
            leds_for_buts[0].blink(on_time=0.2, off_time=0.2, n=1)
        else:
            # the led blinks 3 times when the upper threshold is reached
            leds_for_buts[0].blink(on_time=0.1, off_time=0.1, n=3)
    if pin_num == 17:
        if 1 < val < 9:
            file.write(str(val-1))
            # the led blinks 1 time when you click the button
            leds_for_buts[1].blink(on_time=0.2, off_time=0.2, n=1)
        else:
            # the led blinks 3 times when the lower threshold is reached
            leds_for_buts[1].blink(on_time=0.1, off_time=0.1, n=3)
    file.close()

file_to_share = open(FILE_TO_SHARE_PATH, 'w')
for switch in switches:
    file_to_share.write(str(int(switch.is_pressed)))
    file_to_share.write(' ')
file_to_share.write('1')
file_to_share.close()

# Python callbacks
# Connect the events of the switches to the above written functions
for switch in switches:
    switch.when_pressed = change_effect
    switch.when_released = change_effect

# Python callbacks
# Connect the events of the buttons to the above written function
for button in buttons:
    button.when_pressed = change_volume
