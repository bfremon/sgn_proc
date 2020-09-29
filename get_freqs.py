#!/usr/bin/python3.6

import numpy as np
import scipy
import pandas as pd
from Log import *

set_dbg_lvl(True)

def get_freqs(t, s, smpl_f):
    '''
    t: time vector of evenly spaced values
    s: signal vector
    return a tuple with f_Hz (frequency) and the corresponding pdf
    '''
    # adapted from https://www.ritchievink.com/blog/2017/04/23/understanding-the-fourier-transform-by-example/
    if len(t) != len(s):
        raise SyntaxError('t and s should have the same lenght')
    if smpl_f < 0.0:
        raise SyntaxError('smpl_freq must be a positive float')
    smpl_inter = t[1] - t[0] # sampling interval
    smpl_nb = s.size
    f_Hz = np.linspace(0, 1 / smpl_inter, smpl_nb)[:smpl_nb // 2]
    raw_pdf  = np.abs(np.fft.fft(s))[:smpl_nb // 2]
    norm_pdf = raw_pdf / np.sum(raw_pdf)
    return (f_Hz, norm_pdf)


def get_main_freqs(x_Hz, pdf, thres=0.05):
    '''
    Return all frequencies from (f_Hz, pdf) above thres
    x_Hz: frequency vector
    pdf: pdf of frequencies
    '''
    df = pd.DataFrame({'freq': x_Hz, 'pdf': pdf})
    ret = df[df['pdf'] >= thres]
    return ret['freq']

