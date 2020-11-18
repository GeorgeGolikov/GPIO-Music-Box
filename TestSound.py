import math

import matplotlib.pyplot as plt
import pyaudio
import numpy as np
from queue import Queue

CHUNK = 128
RATE = 44100
LEN = 2
f0 = 400
n = 0
delayT = 0.5
dist = False
robot = False
delay = False

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Отбрасываем "грязный" первичный сигнал
for i in range(500):  # go for a LEN seconds
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    player.write(data, CHUNK)

q = Queue()
# Создание пустых массивов
past = np.empty(500*CHUNK)
now = np.empty(500*CHUNK)
echo = np.empty(500*CHUNK)

# Делаем 500 измерений и добавляем их в буфер
for i in range(500):
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    q.put(data)
    for a in range(CHUNK):
        past[i*CHUNK+a] = data[a] # добавляем в массив чистый сигнал
    player.write(data, CHUNK)

# Делаем новые 500 измерений
for i in range(500):
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    for a in range(CHUNK):
        now[i*CHUNK+a] = data[a] # добавляем в массив чистый сигнал
    data1 = q.get()
    for a in range (CHUNK):
        data[a] = int(data[a] + data1[a]*delayT)
    for a in range(CHUNK):
        echo[i*CHUNK+a] = data[a] # добавляем в массив сигнал с эхо
    player.write(data, CHUNK)

x = np.linspace(0, 10, 50)
y = x
plt.title("Звуковая волна из буфера")  # заголовок
plt.grid()  # включение отображение сетки
plt.plot(past)  # построение графика
plt.show()

x = np.linspace(0, 10, 50)
y = x
plt.title("Звуковая волна текущая")  # заголовок
plt.grid()  # включение отображение сетки
plt.plot(now)  # построение графика
plt.show()

x = np.linspace(0, 10, 50)
y = x
plt.title("Звуковая волна c эффектом эхо")  # заголовок
plt.grid()  # включение отображение сетки
plt.plot(echo)  # построение графика
plt.show()

# Делаем ещё одно измерение
for i in range(1):
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    player.write(data, CHUNK)

data2 = data

plt.title("Чистая звуковая волна")  # заголовок
plt.grid()  # включение отображение сетки
plt.plot(data)  # построение графика
plt.show()

for a in range(CHUNK):
    data2[a] = int(math.atan(float(data[a])/100)*2000)

plt.title("Звуковая волна после эффекта Перегрузки")  # заголовок
plt.grid()  # включение отображение сетки
plt.plot(data2)  # построение графика
plt.show()


for a in range(CHUNK):
    n += 1
    data[a] = int((data[a]) * math.cos(2 * math.pi * f0 * n / RATE))

plt.title("Звуковая волна после эффекта Робота")  # заголовок
plt.grid()  # включение отображение сетки
plt.plot(data2)  # построение графика
plt.show()

stream.stop_stream()
stream.close()
p.terminate()
