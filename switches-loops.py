# switches - gpios
# 1 - 10
# 2 - 9
# 3 - 11

import pygame
import time
from gpiozero import Button, LED
from test import Action, led_blink

pygame.init()

FILE_TO_SHARE_PATH = "./file_to_share.txt"
        
def change_state(device):
    pin_num = device.pin.number
    file = open(FILE_TO_SHARE_PATH, 'r+')
    if pin_num == 10:
        file.seek(0)
    if pin_num == 9:        
        file.seek(2)
    if pin_num == 11:
        file.seek(4)            
    file.write(str(int(device.is_pressed)))
    file.close()

switches = [Button(10), Button(9), Button(11)]

file_to_share = open(FILE_TO_SHARE_PATH, 'w')
for switch in switches:
    file_to_share.write(str(int(switch.is_pressed)))
    file_to_share.write(' ')
file_to_share.write('5')
file_to_share.close()

for switch in switches:
    switch.when_pressed = change_state
    switch.when_released = change_state