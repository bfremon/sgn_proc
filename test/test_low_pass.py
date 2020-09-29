#!/usr/bin/python3

import unittest
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from Log import *
import low_pass

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
        self.assertRaises(SyntaxError, low_pass.blackman, x, self.s, 0.1, 0.1, 0.08)
        self.assertRaises(SyntaxError, low_pass.blackman, self.t, self.s, -0.1, 0.1, 0.1)
        self.assertRaises(SyntaxError, low_pass.blackman, self.t, self.s, 0.1, -0.1, 0.1)
        self.assertRaises(SyntaxError, low_pass.blackman, self.t, self.s, 0.1, -0.1, -0.1)
        self.assertRaises(SyntaxError, low_pass.blackman, self.t, self.s, 0.1, -0.1, -0.1)
        self.assertRaises(SyntaxError, low_pass.blackman, self.t, self.s, 0.1, 1.0, -0.1)
        # cutoff at 50 Hz normalized to smpl_f
        cut_f = self.smpl_f / 20 / self.smpl_f
        bw = cut_f - cut_f / 10
        filtered_s = low_pass.blackman(self.t, self.s, self.smpl_f, cut_f, bw)
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
            
