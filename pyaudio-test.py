import pyaudio
import numpy as np

CHUNK = 2**5
RATE = 44100
LEN = 10

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    print((i, dev['name'], dev['maxInputChannels'], dev['maxOutputChannels']), dev['defaultSampleRate'])

stream = p.open(input_device_index=0,format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)
player = p.open(output_device_index=2, format=pyaudio.paInt16, channels=1, rate=48000, output=True, frames_per_buffer=CHUNK)

for i in range(int(LEN*RATE/CHUNK)): #go for a LEN seconds
    #data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False),dtype=np.int16)
    data = stream.read(CHUNK, exception_on_overflow=False)
    print(data)
    player.write(data)

stream.stop_stream()
stream.close()
p.terminate()