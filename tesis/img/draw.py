#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 17:04:06 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import matplotlib.pyplot as plt

mui= 35
muj= 30
sigma = 25/3
leng = 1000

pi = np.linspace(-mui,3*mui,leng)
pj = np.linspace(-muj,3*muj,leng)


plt.plot(pi,pi,c='grey',linewidth=2,linestyle='--')
plt.plot(pi-10,pi,c='grey',linewidth=1,linestyle='--')
plt.plot(pi+10,pi,c='grey',linewidth=1,linestyle='--')

plt.annotate(s='', xy=(45,56), xytext=(45,34), arrowprops=dict(arrowstyle='<->'))
plt.annotate(s='', xy=(35,45), xytext=(55,45), arrowprops=dict(arrowstyle='<->'))
plt.annotate(s='', xy=(25,25), xytext=(28.5,18), arrowprops=dict(arrowstyle='<->'))

plt.fill_between(pi,pi-10,pi+10,facecolor='steelblue', alpha=0.5)
plt.text(27,21,'DM')
plt.text(46,53,'Draw')
plt.text(50,20,'Player $i$ win')
plt.text(15,50,'Player $J$ win')

plt.xlabel('Performance $p_i$')
plt.ylabel('Performance $p_j$')
plt.xlim(mui/3,2*mui)
plt.ylim(mui/3,2*mui)

plt.savefig(f'./{name}.pdf')
