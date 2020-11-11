import math

import pyaudio
import numpy as np
from queue import Queue

CHUNK = 32
RATE = 48000
LEN = 0.9
f0 = 400
n = 0
delayT = 0.5
dist = False
robot = False
delay = False


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)

q = Queue()
for i in range(int(LEN * RATE / CHUNK)):  # go for a LEN seconds
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    q.put(data)
    data1 = data
    player.write(data, CHUNK)

while True:
    f = open('text', 'r+')  # ВОТ ТЕКСТОВЫЙ ФАЙЛИК, ТУТ МЕНЯТЬ НАДО
    lines = f.read().split(' ')
    f.close()
    if lines[0] == '1':
        dist = True
    else:
        dist = False
    if lines[1] == '1':
        robot = True
    else:
        robot = False
    if lines[2] == '1':
        delay = True
    else:
        delay = False
    delayT = int(lines[3])/10
    print(delayT)

    for i in range(int(0.3 * RATE / CHUNK)):
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        n = n + 100
        if dist:
            for a in range(8):
                data[a*4] = int(math.atan(float(data[a*4])/100)*1000)
                for b in range(3):
                    data[a * 4 + b + 1] = data[a*4]
        if robot:
            for a in range(8):
                data[a * 4] = int((data[a * 4]) * math.cos(2 * math.pi * f0 * n / RATE))
                for b in range(3):
                    data[a * 4 + b + 1] = data[a * 4]
        if delay:
            data1 = q.get()
            for a in range (32):
                data[a] = int(data[a] + data1[a]*delayT)
            q.put(data)
        player.write(data, CHUNK)

stream.stop_stream()
stream.close()
p.terminate()


