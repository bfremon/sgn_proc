#!/usr/bin/python3

import unittest
import numpy as np
from Log import *
import get_freqs

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
        self.assertRaises(SyntaxError, get_freqs.get_freqs, x, self.s, 3.0)
        self.assertRaises(SyntaxError, get_freqs.get_freqs, self.t, self.s, -3.0)
        x, freqs = get_freqs.get_freqs(self.t, self.s, self.smpl_freq)
        self.assertTrue(len(x) == self.smpl_freq // 2)
        self.assertAlmostEqual( np.sum(freqs), 1.0, delta = 0.0001)
        
    def test_find_freqs(self):
        x, freqs = get_freqs.get_freqs(self.t, self.s, self.smpl_freq)
        f = get_freqs.get_main_freqs(x, freqs)
        self.assertTrue(self.f1 in f and self.f2 in f)
