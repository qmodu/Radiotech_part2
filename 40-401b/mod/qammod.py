 # -*- coding:utf-8 -*-
__author__ = 'igor'

from numpy import *
import pylab
import random

# input
fd = 200.0              # Частота дискретизации аналогового несущего сигнала
ffd = 500.0             # Частота дискретизации цифрового исходного сигнала
fc = 50.0               # Частота несущей
n = 10                  # Число передаваемых символов
baud = 10.0             # Символьная скорость, бод
duration = 1 / baud     # Длительность импульса
ts = duration * n       # Время сигнала
wc = math.pi * 2 * fc   # Угловая частота несущей

# input signal generation
input_sequence = [random.randint(0, 2) for x in range(0, n)]
input_signal = []
for x in range(0, n):
    input_signal += [input_sequence[x] for y in arange(0, duration, (1.0 / ffd))]
#print input_signal

# signal modulation

qam = []

# apply noise
new_noise = []
for x in xrange(0, len(input_signal)):
    new_noise += [random.uniform(-1.0, 1.0) for x in arange(0, duration, (1.0 / ffd))]
#print new_noise

#print arange(0, ts, (1.0 / ffd))

# graph
def plot_signal(x, y, title, labelx, labely, position):
    pylab.subplot(2, 1, position)
    pylab.plot(x, y)
    pylab.title(title)
    pylab.xlabel(labelx)
    pylab.ylabel(labely)
    pylab.grid(True)


plot_signal(arange(0, ts, (1.0 / ffd)), input_signal, 'Digital sequence', 'time', '', 1)
#plot_signal(arange(0, ts, (1.0 / ffd)), new_noise, 'used noise', 'time', '', 3)

#pylab.show()