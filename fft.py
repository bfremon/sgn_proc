#!/usr/bin/python3.6

import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from Log import *

# adapted from https://www.ritchievink.com/blog/2017/04/23/understanding-the-fourier-transform-by-example/

t = np.linspace(0, 0.5, 500)
s = np.sin(40 * 2 * np.pi * t) + 0.5 * np.sin(90 * 2  * np.pi * t)

fft = np.fft.fft(s)

for i in range(3):
    print("Value at index {}:\t{}".format(i, fft[i + 1]), "\nValue at index {}:\t{}".format(fft.size -1 - i, fft[-1 - i]))

T = t[1] - t[0] # period
N = s.size # nb of samples
f = np.linspace(0, 1 / T, N)

cut_fft = np.where(abs(fft) > 50, abs(fft), 0.0)

x_f = f[:N // 2]
y_f = np.abs(cut_fft)[:N // 2 ] * 1 / N # 1 / N normalization factor
sns.barplot(x_f, y_f)
plt.show()

# https://tomroelandts.com/articles/how-to-create-a-simple-low-pass-filter
