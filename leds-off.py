import pygame
from gpiozero import LED

pygame.init()

leds = [LED(2), LED(3), LED(23)]

for led in leds:
    led.off()

# for led in leds:
#     del led
# del leds