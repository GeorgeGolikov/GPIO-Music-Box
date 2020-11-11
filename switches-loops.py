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

class Switcher:
    def __init__(self):
        self.__dict = {10: False, 9: False, 11: False}
    def set_state(self, switch_num, val):
        self.__dict[switch_num] = val
    def change_state(self, device):
        self.__dict[device.pin.number] = device.is_pressed
    def play(self):                    
        counter = 0
        list_of_states1 = [0,0,0,5]
        list_of_states2 = [0,0,0,5]
        while True:
            for key, val in self.__dict.items():
                list_of_states2[counter] = int(val)
                counter += 1
            if list_of_states2 != list_of_states1:
                file = open(FILE_TO_SHARE_PATH, 'w')
                for state in list_of_states2:
                    file.write(str(state))
                    file.write(' ')
                file.close()
                print(list_of_states2)
                k = 0
                for state in list_of_states2:
                    list_of_states1[k] = state
                    k += 1                
            counter = 0
            time.sleep(1)

# switches_actions = {Button(10): Action("/home/pi/gpio-music-box/samples/drum_snare_hard.wav", 2),
#                     Button(9): Action("/home/pi/gpio-music-box/samples/drum_cowbell.wav", 3),
#                     Button(11): Action("/home/pi/gpio-music-box/samples/bd_fat.wav", 4)}
switcher = Switcher()
switches = [Button(10), Button(9), Button(11)]
for switch in switches:
    switcher.set_state(switch.pin.number, switch.is_pressed)

for switch in switches:
    switch.when_pressed = switcher.change_state
    switch.when_released = switcher.change_state
    
file_to_share = open(FILE_TO_SHARE_PATH, 'w')
file_to_share.write('0 0 0 5')
file_to_share.close()

switcher.play()
    