 # -*- coding:utf-8 -*-
__author__ = 'igor'

import numpy as np

class Sign(object):
    def __init__(self, duration, sr, func):
        self.duration = duration
        self.sr = sr
        self.func = func