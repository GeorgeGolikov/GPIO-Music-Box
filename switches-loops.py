# switches - gpios
# 1 - 10
# 2 - 9
# 3 - 11

import pygame
import time
from gpiozero import Button, LED
from test import Action, led_blink

pygame.init()

class Switcher:
    def __init__(self):
        self.__dict = {10: False, 9: False, 11: False}
    def set_state(self, switch_num, val):
        self.__dict[switch_num] = val
    def change_state(self, device):
        self.__dict[device.pin.number] = device.is_pressed
    def play(self):
        counter = 0
        while True:
            for key, val in self.__dict.items():
                counter += 1
                if val:
                    print(counter, sep='\t', end='')
            counter = 0    
            print(counter)
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
    
switcher.play()
    