# Номера портов GPIO подключенных к устройству на макетной плате
# переключатели - gpios
# 1 - 10
# 2 - 9
# 3 - 11

# кнопки - gpios
# 1 - 4
# 2 - 17

# светодиоды - gpios
# 1 - 2
# 2 - 3
# 3 - 23

import pygame  # импорт библиотеки для игрофикация
# импорт классов для светдодиодов, переключателей и кнопок, чтобы соединить их со скриптом
from gpiozero import Button, LED
import math
import pyaudio
import numpy as np
from queue import Queue

pygame.init()
p = pyaudio.PyAudio()

NUM_LEDS_SWITCHES = 3
# писки объектов LED и Button, представляющих физические устройства. Аргумент конструктора - номер порта gpio
leds = [LED(2), LED(3), LED(23)]
switches = [Button(10), Button(9), Button(11)]
buttons = [Button(4), Button(17)]
leds_for_buts = [LED(24), LED(25)]

CHUNK = 32    # - количество сэмплов в буфере
RATE = 44100  # - частота дискретизации
LEN = 0.9     # - длина эхо
f0 = 400      # - коэффициент для робота
n = 0         # - коэффициент для робота
delayT = 0.5  # - коэффициент затухания
dist = False
robot = False
delay = False

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

# цикл для сопоставления значений переключателей со значениями светодиодов в начале этой программы
# переключатель нажат - светодиод горит, переключатель отпущен - светодиод не горит
for i in range(NUM_LEDS_SWITCHES):
    leds[i].value = switches[i].value

# Объявление очереди LIFO для Эхо
q = Queue()
for i in range(int(LEN * RATE / CHUNK)):  # go for a LEN seconds
    # stream read - читает данные из потока, при записи звука
    data = np.fromstring(stream.read(CHUNK), dtype=np.int16)
    # данные добавляются в очередь
    q.put(data)
    # player write - записывает в поток данные при воспроизведении звука
    player.write(data, CHUNK)


# функция изменения звукового эффекта при нажатии переключателя
# принимает объект переключателя в качестве аргумента
def change_effect(device):
    pin_num = device.pin.number  # номер порта gpio
    file = open(FILE_TO_SHARE_PATH, 'r+')
    if pin_num == 10:
        file.seek(0)
        leds[0].toggle()  # изменить состояние 1-го светодиода
    if pin_num == 9:
        file.seek(2)
        leds[1].toggle()  # изменить состояние 2-го светодиода
    if pin_num == 11:
        file.seek(4)
        leds[2].toggle()  # изменить состояние 3-го светодиода
    file.write(str(int(device.is_pressed)))
    file.close()


# функция для изменения длины эха при нажатии кнопки
# принимает объект кнопки в качестве аргумента
def change_volume(device):
    pin_num = device.pin.number
    file = open(FILE_TO_SHARE_PATH, 'r+')
    file.seek(6)
    val = int(file.read())
    file.seek(6)
    print(val)
    if pin_num == 4:
        if 0 < val < 8:
            file.write(str(val + 1))
            # светодиод мигает 1 раз при нажатии на кнопку
            leds_for_buts[0].blink(on_time=0.2, off_time=0.2, n=1)
        else:
            # светодиод мигает 3 раза при достижении верхнего порога
            leds_for_buts[0].blink(on_time=0.1, off_time=0.1, n=3)
    if pin_num == 17:
        if 1 < val < 9:
            file.write(str(val - 1))
            # светодиод мигает 1 раз при нажатии на кнопку
            leds_for_buts[1].blink(on_time=0.2, off_time=0.2, n=1)
        else:
            # светодиод мигает 3 раза при достижении нижнего порога
            leds_for_buts[1].blink(on_time=0.1, off_time=0.1, n=3)
    file.close()


file_to_share = open(FILE_TO_SHARE_PATH, 'w')
for switch in switches:
    file_to_share.write(str(int(switch.is_pressed)))
    file_to_share.write(' ')
file_to_share.write('1')
file_to_share.close()

# Обратные вызовы Python
# Подключиние события переключателей к написанным выше функциям
for switch in switches:
    switch.when_pressed = change_effect
    switch.when_released = change_effect

# Обратные вызовы Python
# Подключение события кнопок к написанной выше функции
for button in buttons:
    button.when_pressed = change_volume

while True:

    # dist = ?
    # robot = ?
    # delay = ?
    # delayT = ?

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
