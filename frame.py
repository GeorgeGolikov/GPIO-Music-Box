# switches - gpios
# 1 - 10
# 2 - 9
# 3 - 11

import pygame
import time
from gpiozero import Button, LED
from test import Action, led_blink

pygame.init()

# leds = [LED(2), LED(3), LED(23), LED(24), LED(25)]

# switches_actions = {Button(10): Action("/home/pi/gpio-music-box/samples/drum_snare_hard.wav", 2),
#                     Button(9): Action("/home/pi/gpio-music-box/samples/drum_cowbell.wav", 3),
#                     Button(11): Action("/home/pi/gpio-music-box/samples/bd_fat.wav", 4)}

switches_actions = {Button(10): LED(2),
                    Button(9): LED(3),
                    Button(11): LED(23)}

for switch, action in switches_actions.items():
    switch.when_pressed = action.on
    switch.when_released = action.off