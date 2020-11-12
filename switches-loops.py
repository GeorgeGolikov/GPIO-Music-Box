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

import pygame
from gpiozero import Button, LED

pygame.init()

FILE_TO_SHARE_PATH = "./file_to_share.txt"
NUM_LEDS_SWITCHES = 3

leds = [LED(2), LED(3), LED(23)]
switches = [Button(10), Button(9), Button(11)]
buttons = [Button(4), Button(17)]

for i in range(NUM_LEDS_SWITCHES):
    leds[i].value = switches[i].value

def change_effect(device):
    pin_num = device.pin.number
    file = open(FILE_TO_SHARE_PATH, 'r+')
    if pin_num == 10:
        file.seek(0)
        leds[0].toggle()
    if pin_num == 9:        
        file.seek(2)
        leds[1].toggle()
    if pin_num == 11:
        file.seek(4)
        leds[2].toggle()
    file.write(str(int(device.is_pressed)))
    file.close()
    
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
    if pin_num == 17:
        if 1 < val < 9:
            file.write(str(val-1))
    file.close()

file_to_share = open(FILE_TO_SHARE_PATH, 'w')
for switch in switches:
    file_to_share.write(str(int(switch.is_pressed)))
    file_to_share.write(' ')
file_to_share.write('8')
file_to_share.close()

for switch in switches:
    switch.when_pressed = change_effect
    switch.when_released = change_effect
    
for button in buttons:
    button.when_pressed = change_volume
