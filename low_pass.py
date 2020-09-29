#!/usr/bin/python3.6

import numpy as np
from Log import *

set_dbg_lvl(True)

def blackman(s, t, smpl_f,  f_c, bw):
    '''
    t: time vector of evenly spaced values
    s: signal vector
    f_c: normalized cut off frequency (express in percent of sampling rate)
    bw: bandwith
    '''
    # https://tomroelandts.com/articles/how-to-create-a-simple-low-pass-filter
    if len(t) != len(s):
        raise SyntaxError('t and s should have the same lenght')
    if f_c < 0.0 or bw < 0.0 or smpl_f < 0.0: 
        raise SyntaxError('f_c, smpl_f, and bw must be strictly positive floats')
    if f_c < bw:
        raise SyntaxError('bw must be superior or equal to f_c')
    if f_c > 1.0:
        raise SyntaxError('f_c must be strictly inferior to 1.0')
    dbg('normalized cut_f: %3.1f (absolute: %3.1f Hz)' % (f_c, f_c * smpl_f))
    # N window length : 4 / bw is an heuristic
    N = int(np.ceil(4 / bw))
    if not N % 2:
        N += 1
    dbg('window len:', N)
    n = np.arange(N)
    h = np.sinc(2 * f_c * (n - (N - 1) / 2))
    h *= np.blackman(N)
    # normalisation : gain = 1
    h /= np.sum(h)
    cut_s = np.convolve(s, h) #[:int(N-1) // 2]
    dbg(len(cut_s))
    return cut_s
    # signal shifted by window len
#    return cut_s[int(N-1):]


if __name__ == '__main__':
    import unittest
    import matplotlib.pyplot as plt
    import seaborn as sns

    class test_filters(unittest.TestCase):
        smpl_f = 1000
        t = np.linspace(0, 1, smpl_f)
        f1 = 40
        s1 = np.sin(f1 * 2 * np.pi * t)
        f2 = 90
        s2 = np.sin(f2 * 2  * np.pi * t)
        s = s1 + 0.5 * s2
        
        def test_blackman(self):
            x = np.append(self.t, ['1'])
            self.assertRaises(SyntaxError, blackman, x, self.s, 0.1, 0.1, 0.08)
            self.assertRaises(SyntaxError, blackman, self.t, self.s, -0.1, 0.1, 0.1)
            self.assertRaises(SyntaxError, blackman, self.t, self.s, 0.1, -0.1, 0.1)
            self.assertRaises(SyntaxError, blackman, self.t, self.s, 0.1, -0.1, -0.1)
            self.assertRaises(SyntaxError, blackman, self.t, self.s, 0.1, -0.1, -0.1)
            self.assertRaises(SyntaxError, blackman, self.t, self.s, 0.1, 1.0, -0.1)
            # cutoff at 50 Hz normalized to smpl_f
            cut_f = self.smpl_f / 20 / self.smpl_f
            bw = cut_f - cut_f / 10
            filtered_s = blackman(self.t, self.s, self.smpl_f, cut_f, bw)
            dbg(len(filtered_s))
            dbg(len(self.s))
            self.assertTrue(len(filtered_s) == len(self.s))
            plt.show()
            self._plt_blackman(self.s1, self.s2, self.s, filtered_s)

        def _plt_blackman(self, s1, s2, s, cut_s):
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex = True, sharey = True)
            sns.lineplot(self.t, self.s1, ax = ax1)
            sns.lineplot(self.t, self.s2, ax = ax2)
            sns.lineplot(self.t, self.s, ax = ax3)
            sns.lineplot(self.t, cut_s, ax = ax4)
            plt.show()
            
    unittest.main()
        


