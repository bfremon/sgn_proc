#!/usr/bin/python3.6

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# https://tomroelandts.com/articles/how-to-create-a-simple-low-pass-filter

# 500 / 0.5 = 1000 Hz sampling
t = np.linspace(0, 0.5, 500)

# s1 at 40 Hz, s2 at 90 Hz
s1 = np.sin(40 * 2 * np.pi * t)
s2 = 0.5 * np.sin(90 * 2  * np.pi * t) 
s = s1 + s2

# f_c: cut off frequency (% of sampling)
f_c = 0.05
bw = 0.045

# filter length : 4 / bw is an heuristic
N = int(np.ceil(4 / bw))
if not N % 2: N += 1
n = np.arange(N)

h = np.sinc(2 * f_c * (n - (N - 1) / 2))

h = h * np.blackman(N)

# normalisation : gain = 1
h = h / np.sum(h)

cut_s = np.convolve(s, h)

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex = True, sharey = True)
sns.lineplot(t, s1, ax = ax1)
sns.lineplot(t, s2, ax = ax2)
sns.lineplot(t, s, ax = ax3)

# delay : caused by length of filter (N - 1) / 2

sns.lineplot(t, cut_s[:int((N-1) / 2)], ax = ax4)
plt.show()
