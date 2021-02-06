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
print('Partidas totales ', df_TTT_h.shape[0])

print('Partidas con posible cambio de color', df_TTT_h[df_TTT_h.handicap_prediction < 1 ].shape[0])
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

print("Partidas en intervalo 0-25 y 75-100 ", sum(frec[0:25])+sum(frec[70:]))
print("Partidas en intervalo 25-75 ", sum(frec[25:70]))

fig = plt.figure(0)
ax1 = fig.add_subplot(111)
ax1.scatter(x, y, color='steelblue',  alpha=0.5, label='Predicted percentage black win')
plt.plot([0, 100], [0, 100], linestyle='--', color='k', label='Identity')
plt.axvline(x=50, linestyle='--', color='firebrick')
#ax1.scatter(y_noH, x_noH, color='firebrick', alpha=0.5, label='No Handicap')
ax1.set_xlabel('Estimated probability of black win')
ax1.set_ylabel('Frec of black winning')
ax1.set_xticks(ticks)
ax1.set_yticks(ticks)
plt.legend()

plt.savefig(f'{name}_sigmoide.pdf', dpi=100)


# utilizando las estimaciones reales y no la lineal.
# es la frecuencia en que sucede una probabilidad estimada
# ademas pongo la frencuencia con las que ganan partidas
#df_TTT_h = pd.read_csv('./Datos/TTT_H_analizada_real.csv')

fig = plt.figure(1)
ax = fig.add_subplot(111)
df_TTT_h[df_TTT_h.handicap_prediction >= 1 ].hist(column='proba', bins=bins, color='forestgreen', ax=ax, alpha=0.5,
              label='Estimations with \n proposed handicap', edgecolor='black',density=True)
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
plt.savefig(f'{name}_hist_prob_real.pdf', dpi=100)

fig = plt.figure(11)
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

fig = plt.figure(12)
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

'''
# no estaria dando...
fig = plt.figure(2)
ax1 = fig.add_subplot(111)

 # da una gaussiana en 40
hist2,bin_edges2 = np.histogram(df_TTT_h.loc[df_TTT_h.black_win ==1, 'proba_real'],  bins=bins, density=True)
hist, bin_edges = np.histogram(df_TTT_h.proba_real,  bins=bins, density=True)
mu, std = norm.fit(hist)

p = norm.pdf(bin_edges[:-1], mu, std)
plt.plot(x, p, 'k', linewidth=2)
plt.bar(bin_edges[:-1], height=hist)
plt.bar(bin_edges2[:-1], height=hist2)
#hist,bin_edges = np.histogram(df_TTT_h[df_TTT_h.handicap_prediction >= 1 ], 'proba', bins=bins, density=True)
#hist,bin_edges = np.histogram(df_TTT_h[df_TTT_h.black_win==1], 'proba_real', bins=bins, density=True)

ax1.set_xlabel('Estimate probability of black win')
ax1.set_ylabel('Frequency')
ax1.set_xticks(ticks)
ax1.set_yticks([])
plt.title(" ")
plt.legend()
'''



print('Partidas totales: ', df_TTT_h.shape[0])
print('Partidas ganadas por negro: ', df_TTT_h.black_win.sum())


print('media ideal', df_TTT_h.proba.mean())
print('media real estimada', df_TTT_h.proba_real.mean())
print('media black win', df_TTT_h[df_TTT_h.black_win==1].proba_real.mean())
###############################################################################
bins = 15
fig = plt.figure(3)
ax = fig.add_subplot(111)
df_TTT_h[df_TTT_h.handicap==3].hist(column='proba_real', bins=bins, color='firebrick', ax=ax,
              alpha=0.5, label='Given handicap', edgecolor='black') # da una gaussiana en 40
ax.set_xlabel('Estimate probability of black win')
ax.set_ylabel('Frequency')
plt.legend()
plt.savefig(f'{name}_hist_prob_real_H3.pdf', dpi=100)

fig = plt.figure(4)
ax = fig.add_subplot(111)
df_TTT_h[(df_TTT_h.handicap_prediction==3)].hist(column='proba_real', bins=bins, color='firebrick', ax=ax,
              alpha=0.5, label='Optimal handicap', edgecolor='black') # da una gaussiana en 40
ax.set_xlabel('Estimate probability of black win')
ax.set_ylabel('Frequency')
plt.legend()
plt.savefig(f'{name}_hist_probs_estimado_H3.pdf', dpi=100)

fig = plt.figure(5)
ax = fig.add_subplot(111)
df_TTT_h[(df_TTT_h.handicap==3)  & (df_TTT_h.handicap_prediction==3)].hist(column='proba_real', bins=bins, color='firebrick', ax=ax,
              alpha=0.5, label='Given handicap', edgecolor='black') # da una gaussiana en 40
ax.set_xlabel('Estimate probability of black win')
ax.set_ylabel('Frequency')
plt.legend()
plt.savefig(f'{name}_hist_prob_realestimado_H3-3.pdf', dpi=100)



print('h3 de menos:', round(100*df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==4)].black_win.sum()/df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==4)].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==4)].proba_real.mean(),2), '%')
print('h3 bien:', round(100*df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==3)].black_win.sum()/df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==3)].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==3)].proba_real.mean(),2), '%')

print('h3 de mas:', round(100*df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==2)].black_win.sum()/df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==2)].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[(df_TTT_h.handicap==3)&(df_TTT_h.handicap_prediction==2)].proba_real.mean(),2), '%')


print('cantidad de partidas ganadas con h1:', round(100*df_TTT_h[df_TTT_h.handicap==1].black_win.sum()/df_TTT_h[df_TTT_h.handicap==1].shape[0],2),
'%  | proba calculada: ', round(df_TTT_h[df_TTT_h.handicap==1].proba_real.mean(),2), '%')
print('cantidad de partidas ganadas con h2:', round(100*df_TTT_h[df_TTT_h.handicap==2].black_win.sum()/df_TTT_h[df_TTT_h.handicap==2].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[df_TTT_h.handicap==2].proba_real.mean(),2), '%')
print('cantidad de partidas ganadas con h3:', round(100*df_TTT_h[df_TTT_h.handicap==3].black_win.sum()/df_TTT_h[df_TTT_h.handicap==3].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[df_TTT_h.handicap==3].proba_real.mean(),2), '%')
print('cantidad de partidas ganadas con h4:', round(100*df_TTT_h[df_TTT_h.handicap==4].black_win.sum()/df_TTT_h[df_TTT_h.handicap==4].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[df_TTT_h.handicap==4].proba_real.mean(),2), '%')
print('cantidad de partidas ganadas con h5:', round(100*df_TTT_h[df_TTT_h.handicap==5].black_win.sum()/df_TTT_h[df_TTT_h.handicap==5].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[df_TTT_h.handicap==5].proba_real.mean(),2), '%')
print('cantidad de partidas ganadas con h6:', round(100*df_TTT_h[df_TTT_h.handicap==6].black_win.sum()/df_TTT_h[df_TTT_h.handicap==6].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[df_TTT_h.handicap==6].proba_real.mean(),2), '%')
print('cantidad de partidas ganadas con h7:', round(100*df_TTT_h[df_TTT_h.handicap==7].black_win.sum()/df_TTT_h[df_TTT_h.handicap==7].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[df_TTT_h.handicap==7].proba_real.mean(),2), '%')
print('cantidad de partidas ganadas con h8:', round(100*df_TTT_h[df_TTT_h.handicap==8].black_win.sum()/df_TTT_h[df_TTT_h.handicap==8].shape[0],2),
'%  | proba calculada: ',round(df_TTT_h[df_TTT_h.handicap==8].proba_real.mean(),2), '%')
'''
# data with no handicap
bins = 100
df_TTT['proba_real_bins'] = pd.cut(df_TTT['proba'], bins)
df_TTT['proba_real_bins'] = df_TTT.groupby('proba_real_bins')['proba'].transform('mean')
df_TTT.sort_values('proba_real_bins', inplace=True)
frec_black = df_TTT.groupby('proba_real_bins')['black_win'].sum().tolist()
frec = df_TTT.groupby('proba_real_bins').size().tolist()
y_noH = 100 * np.array(frec_black) / np.array(frec)
x_noH = df_TTT.groupby('proba_real_bins')['proba_real_bins'].transform(tuple).unique().tolist()
'''
