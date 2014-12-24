 # -*- coding:utf-8 -*-
__author__ = 'igor'

import numpy as np
import pylab as plt
import random
from sign import Sign

class Qam:

    def __init__(self, fd, ffd, n,
            modulation = {'0':(0, 0), '1':{1, 0}},
            baud = 10,
            bpb = 1,
            fc = 50):

        self.modulation   = modulation
        self.baud         = baud                   # Символьная скорость, бол
        self.bpb          = bpb                    # Бит на бод
        self.fc           = fc                     # Частота несущей
        self.noise        = []                     # Шум
        self.input_signal = []                     # Сигнал, входящий на устройство модуляции
        self.fd           = fd                     # Частота дискретизации аналогового несущего сигнала
        self.ffd          = ffd                    # Частота дискретизации цифрового исходного сигнала
        self.n            = n                      # Число передаваемых символов
        self.wc           = np.pi * 2 * self.fc    # Угловая частота несущей
        self.duration     = 1 / self.baud          # Длительность импульса
        self.ts           = self.duration * n      # Время сигнала

    '''
    def generate_signal(self, data):
        def create_func(data):
            slot_data = []
            for i in range(0, len(data), self.bpb):
                slot_data.append(self.modulation[data[i:i+self.bpb]])

            def timefunc(t):
                slot = int(t * self.baud)
                start = float(slot) / self.baud
                offset = t - start
                amplitude,phase = slot_data[slot]
                return amplitude * np.sin(2 * np.pi * self.fc * offset +
                        phase / 180.0 * np.pi)

            return timefunc

        func = create_func(data)
        duration = float(len(data)) / (self.baud * self.bpb)
        s = Sign(duration = duration, func = func)
        return s                                    # return signal
    '''
    def mod(self):
        return

    def generate_noise(self):
        for x in xrange(0, len(self.input_signal)):
            self.noise += [random.uniform(-1.0, 1.0) for x in
                           np.arange(0, self.duration, (1.0 / self.ffd))]

    def demod(self):

        print "Result: \n"

    '''
    def plot_constellation(self):
        data = [(a * np.cos(p / 180.0 * np.pi), a * np.sin(p / 180.0 * np.pi), t)
                for t,(a,p) in self.modulation.items()]
        sx, sy, t = zip(*data)
        plt.clf()
        plt.scatter(sx,sy,s=30)
        plt.axes().set_aspect('equal')
        for x,y,t in data:
            plt.annotate(t,(x-.03,y-.03), ha='right', va='top')
        plt.axis([-1.5,1.5,-1.5,1.5])
        plt.axhline(0, color='red')
        plt.axvline(0, color='red')
        plt.grid(True)
    '''