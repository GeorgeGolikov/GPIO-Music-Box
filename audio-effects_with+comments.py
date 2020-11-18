import math

import pyaudio
import numpy as np
from queue import Queue

CHUNK = 32    # - количество сэмплов в буфере
RATE = 44100  # - частота дискретизации
LEN = 0.9     # - длина эхо
f0 = 400      # - коэффициент для робота
n = 0         # - коэффициент для робота
delayT = 0.5  # - коэффициент затухания
dist = False
robot = False
delay = False
share_file_path = 'D:\\microprocessors_file\\file_to_share.txt'

# создание экземпляра основного объекта модуля Pyaudio
# который предоставляет возможность работы со звуком
p = pyaudio.PyAudio()

# open возвращает объект Stream, открывает поток на воспроизведение или чтение звука.
# Параметры:
# format – тип сэмплов - 16 битный int
# channels – количество каналов (2 - Стерео; 1 - Моно)
# rate - частота дискретизации
# input - true если это аудио вход
# output - true если это аудио выход
# frames_per_buffer количество сэмплов в буфере

# входной поток
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
# выходной поток
player = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, output=True, frames_per_buffer=CHUNK)

# Объявление очереди LIFO для Эхо
q = Queue()
for i in range(int(LEN * RATE / CHUNK)):  # go for a LEN seconds
    # stream read - читает данные из потока, при записи звука
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    # данные добавляются в очередь
    q.put(data)
    # player write - записывает в поток данные при воспроизведении звука
    player.write(data, CHUNK)

while True:
    f = open(share_file_path, 'r')
    lines = f.read().split(' ')
    f.close()
    if len(lines) > 1:
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
        # читаем из выходного потока новые данные
        data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
        # изменяем коэффициент для робота
        n = n + 100
        if dist:
            # цикл по массиву из сэмплов
            for a in range(CHUNK):
                # c помощью нахождения артангенса от каждого сэмпла
                # получается эффект перегрузки
                # первоначальным делением, а затем умножением значения достигается наиболее выраженный эффект
                data[a] = int(math.atan(float(data[a]) / 100) * 2000)
        if robot:
            # цикл по массиву из сэмплов
            for a in range(CHUNK):
                # каждый сэмпл умножается на формулу math.cos(2 * math.pi * f0 * n / RATE))
                # в которой на каждой итерации варьируется n
                # изза чего получается искажение звука
                # что приводит к эффекту робота
                data[a] = int((data[a]) * math.cos(2 * math.pi * f0 * n / RATE))
        if delay:
            # берётся первый элемент из очереди
            data1 = q.get()
            # цикл по массиву из сэмплов
            for a in range(CHUNK):
                # поэлементно складываем массивы текущего звука, и звука из буфера умноженного на
                # коэффициент затухания
                data[a] = int(data[a] + data1[a] * delayT)
            # добавляем новое значение звука в начала очереди
            q.put(data)
        # записываем на выходной поток данные с наложенными эффектами
        player.write(data, CHUNK)

# завершаем поток
stream.stop_stream()
# закрываем поток
stream.close()
# закрываем объект PyAudio
p.terminate()
