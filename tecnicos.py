# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 23:27:28 2020

@author: gerar
"""

import pandas as pd
import numpy as np


def SMA(serie, n):
    """  SIMPLE Moving Average
    serie y numero de lag"""

    return serie.rolling(window=n).mean()


def EMA(serie, n):
    """  Exponential Moving Average
    serie y numero de lag"""

    ewm = serie.ewm(n, adjust=False).mean()
    ewm[0:n] = [np.nan]*n
    return ewm


def WMA(serie, n=10):
    """ Weighted Moving Average
    serie y numero de lag"""
    wg = np.arange(1, n+1)
    wma = serie.rolling(n).apply(lambda x: np.dot(x, wg)/wg.sum(), raw=True)

    return wma


def BOLLINGER(serie, n):
    std = pd.Series(pd.Series.rolling(serie, n).std(), name='STD' + str(n))
    sma = SMA(serie, n)
    upperB = pd.Series(sma + std * 2, name='UBand')
    lowerB = pd.Series(sma + std * 2, name='LBand')
    
    return sma.to_frame().join(upperB).join(lowerB)


def RSI(serie, n=14):
    diff = serie.diff().fillna(0)
    up = diff.clip(lower=0)
    lw = diff.clip(upper=0)*-1

    mmup = EMA(up, n)
    mmlw = EMA(lw, n)

    return 100 - (100/(1 + mmup/mmlw))


def TAS(px, high, low, w=10, n=3):
    """ STOCHASTIC OSCILLATOR
    precios, precios high, precios low, window, n de la media movil
    """

    minn = low.rolling(window=w).min()  # min de minimos
    maxx = high.rolling(window=w).max()  # max de maximos

    k = 100 * (px - minn) / (maxx - minn)
    d = SMA(k, n)
    return k, d


def TASS(px, high, low, w=10, n=3, slow=3):
    """ SLOW STOCHASTIC OSCILLATOR
    precios, precios high, precios low, window, n de la media movil
    """
    k, _ = TAS(px, high, low, w, n)
    k = SMA(k, slow)  # suavizo stochastic
    d = SMA(k, n)
    return k, d

def MACD(serie, c=12, l=16):
    emaC = EMA(serie, c)
    emaL = EMA(serie, l)
    return emaC -emaL

