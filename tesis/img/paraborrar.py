#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
black_win es 1 si gano el negro.
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import norm
import os
name = os.path.basename(__file__).split(".py")[0]


df_TTT_h = pd.read_csv('./Datos/TTT_H_analizada.csv')
print('partidas con posible cambio de color', df_TTT_h[df_TTT_h.handicap_prediction < 1 ].shape[0])
# Fit a normal distribution to the data:
"""
tot = df_TTT_h.shape[0]
conH =  df_TTT_h[(df_TTT_h.handicap >1)].shape[0]
conH_dist = df_TTT_h[(df_TTT_h.handicap == df_TTT_h.handicap_prediction)].shape[0]
print(100*conH_dist/conH)
"""
bins = 100
df_TTT_h['proba_real_bins'] = pd.cut(df_TTT_h['proba_real'], bins)
df_TTT_h['proba_real_bins'] = df_TTT_h.groupby('proba_real_bins')['proba_real'].transform('mean')
df_TTT_h.sort_values('proba_real_bins', inplace=True)
frec_black = np.array(df_TTT_h.groupby('proba_real_bins')['black_win'].sum().tolist())
frec = np.array(df_TTT_h.groupby('proba_real_bins').size().tolist())
y = 100*frec_black / frec
x = df_TTT_h.groupby('proba_real_bins')['proba_real_bins'].transform(tuple).unique().tolist()
ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]




# utilizando las estimaciones reales y no la lineal.
# es la frecuencia en que sucede una probabilidad estimada
# ademas pongo la frencuencia con las que ganan partidas
#df_TTT_h = pd.read_csv('./Datos/TTT_H_analizada_real.csv')

fig = plt.figure(1)
ax = fig.add_subplot(111)
df_TTT_h[df_TTT_h.black_win == 1].hist(column='proba_real', bins=bins, color='steelblue', ax=ax,
              alpha=0.5, label='Actual results', edgecolor='black',density=True)

df_TTT_h.hist(column='proba_real', bins=bins, color='firebrick', ax=ax,
              alpha=0.5, label='Estimations with \n actual handicap', edgecolor='black',density=True)
              #weights=np.ones_like(df_TTT_h[df_TTT_h.columns[0]]) * 100. / len(df_TTT_h)) # da una gaussiana en 40

ax.set_xlabel('Probability of black winning')
ax.set_ylabel('Frequency')
ax.set_xticks(ticks)
ax.set_yticks([])
plt.title(" ")
plt.legend()
plt.savefig(f'{name}_hist_prob_real1.pdf', dpi=100)

fig = plt.figure(2)
ax = fig.add_subplot(111)
df_TTT_h[df_TTT_h.handicap_prediction >= 1 ].hist(column='proba', bins=bins, color='forestgreen', ax=ax, alpha=0.5,
              label='Estimations with \n proposed handicap', edgecolor='black',density=True)
df_TTT_h[df_TTT_h.black_win == 1].hist(column='proba_real', bins=bins, color='steelblue', ax=ax,
              alpha=0.5, label='Actual results', edgecolor='black',density=True)

              #weights=np.ones_like(df_TTT_h[df_TTT_h.columns[0]]) * 100. / len(df_TTT_h)) # da una gaussiana en 40

ax.set_xlabel('Probability of black winning')
ax.set_ylabel('Frequency')
ax.set_xticks(ticks)
ax.set_yticks([])
plt.title(" ")
plt.legend()
plt.savefig(f'{name}_hist_prob_real2.pdf', dpi=100)
