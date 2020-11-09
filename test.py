# buttons - gpios
# 1 - 4
# 2 - 17
# 3 - 27
# 4 - 22
# 5 - 18

# leds - gpios
# 1 - 2
# 2 - 3
# 3 - 23
# 4 - 24
# 5 - 25

import pygame
import time
from gpiozero import Button, LED

pygame.init()


leds = [LED(2), LED(3), LED(23), LED(24), LED(25)]
def led_blink(n):
    leds[n].on()
    time.sleep(0.1)
    leds[n].off()

class Action:
    def __init__(self, sound_path, light_num):
        self.__sound = pygame.mixer.Sound(sound_path)
        self.__light = light_num
    def do_action(self):
        led_blink(self.__light)
        self.__sound.play()
        
button_actions = {Button(4): Action("/home/pi/gpio-music-box/samples/drum_tom_mid_hard.wav", 0),
                 Button(17): Action("/home/pi/gpio-music-box/samples/drum_cymbal_hard.wav", 1),
                 Button(27): Action("/home/pi/gpio-music-box/samples/drum_snare_hard.wav", 2),                
                 Button(22): Action("/home/pi/gpio-music-box/samples/drum_cowbell.wav", 3),
                 Button(18): Action("/home/pi/gpio-music-box/samples/bd_fat.wav", 4)}

for button, action in button_actions.items():
    button.when_pressed = action.do_action