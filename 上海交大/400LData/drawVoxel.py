#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 14:28:39 2017

@author: Rao
"""

import numpy as np
from matplotlib.patches import Ellipse, Circle
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)



for i in range(1,5):
    cir=Circle(xy = (0.0, 20.0), radius=2*i, facecolor='none')
    ax.add_patch(cir)

for i in range(1,5):
    cir=Circle(xy = (20.0, 20.0), radius=np.sqrt(i*16), facecolor='none')
    ax.add_patch(cir)

for i in range(1,9):
    cir=Circle(xy = (0.0, 0.0), radius=i, facecolor='none')
    ax.add_patch(cir)

for i in range(1,9):
    cir=Circle(xy = (20.0, 0.0), radius=np.sqrt(i*8), facecolor='none')
    ax.add_patch(cir)



ax.spines['top'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

ax.set_xticks([])  
ax.set_yticks([]) 
plt.axis('scaled')
ax.set_xlim(-10, 30)
ax.set_ylim(-10, 30)
#plt.axis('equal')   #changes limits of x or y axis so that equal increments of x and y have the same length

plt.show()
#plt.savefig('voxel.png', dpi = 300)