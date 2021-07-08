# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:32:52 2021

@author: gerar
"""

import pandas as pd
import numpy as np


def TASS(px, k, d, os=25, ob=75):
    '''
    buy signal: K cruza para arriba D (t = 1) y esta bajo Oversold
    sell signal: K cruza para abajo de D (t = -1) y esta sobre Overbought
    '''
    v = (k / d - 1) * 100
    
  
    
    t = np.where(np.isnan(d), 0, np.where(k >= d, 1, -1))
    t = t - np.roll(t, 1)  # np.roll es igual a shift
    t[0] = 0  # primer valor debe ser 0, empezar neutral
    t = np.where(t > 0, 1, np.where(t < 0, -1, 0))  # dice cuando se cruzan

    t = np.where(np.isnan(t), np.nan,
                 np.where((k < os) & (t == 1), 1,
                          np.where((k > ob) & (t == -1), -1, 0)))


