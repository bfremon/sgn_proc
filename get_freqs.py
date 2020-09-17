#!/usr/bin/python3.6

import numpy as np
import scipy
import pandas as pd
from Log import *

set_dbg_lvl(True)

def get_freqs(t, s, smpl_freq):
    '''
    t: time vector of evenly spaced values
    s: signal vector
    return a tuple with f_Hz (frequency) and the corresponding pdf
    '''
    # adapted from https://www.ritchievink.com/blog/2017/04/23/understanding-the-fourier-transform-by-example/
    if len(t) != len(s):
        raise SyntaxError('x and y should have the same lenght')
    if smpl_freq < 0.0:
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

    
if __name__ == '__main__':

    import unittest
    
    class test_get_freqs(unittest.TestCase):

        smpl_freq = 1000
        t = np.linspace(0, 1, smpl_freq)
        f1 = 40
        s1 = np.sin(f1 * 2 * np.pi * t)
        f2 = 90
        s2 = np.sin(f2 * 2  * np.pi * t)
        s = s1 + 0.5 * s2
        
        def test_get_freqs(self):
            x = np.append(self.t, ['1'])
            self.assertRaises(SyntaxError, get_freqs, x, self.s, 3.0)
            self.assertRaises(SyntaxError, get_freqs, self.t, self.s, -3.0)
            x, freqs = get_freqs(self.t, self.s, self.smpl_freq)
            self.assertTrue(len(x) == self.smpl_freq // 2)
            self.assertAlmostEqual( np.sum(freqs), 1.0, delta = 0.0001)
            
        def test_find_freqs(self):
            x, freqs = get_freqs(self.t, self.s, self.smpl_freq)
            f = get_main_freqs(x, freqs)
            self.assertTrue(self.f1 in f and self.f2 in f)

    unittest.main()
