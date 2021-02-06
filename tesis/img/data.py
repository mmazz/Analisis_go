#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:35:58 2020

@author: mati
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
name = os.path.basename(__file__).split(".py")[0]

# Comentado para adaptar a archivo bajado del repo.
#df = pd.read_csv('KGS_filtered.csv')
df = pd.read_csv('KGS_filtered.csv')
total = df.shape[0]

# saber si voy a hacer visualizacion solo con la base entera o con la de no komi
df0 = pd.read_csv('KGS_filtered_NoKomi.csv')
print(df0.shape[0])
total = df0.shape[0]
print('sin komi con H', df0[df0.handicap>0].groupby('handicap').handicap.count().sum()*100/total)
print('sin komi sin H', df0[df0.handicap==0.0].groupby('handicap').handicap.count().sum()*100/total)
total = df.shape[0]
print(total)
# veo cuantos hay con bots y se los saco

print(df[df.komi==0.5].shape[0]*100/total)


#df=df[:50]
# sacar bots?
print(df.shape)
df = df[df.komi>0]
#print(df.shape)
df = df[df.komi<10]
print(df.shape)
#%%
print('rank')
# veo cuantos tienen alguna partida contra un rango pro y cuantas son solo entre rango pro
print(df[(df.whiteRank.str.contains('p',case=False, na=False))&(df.blackRank.str.contains('p',case=False, na=False))].shape[0])
print(df[(df.whiteRank.str.contains('p',case=False, na=False))|(df.blackRank.str.contains('p',case=False, na=False))].shape[0])

total = df.shape[0]
# miro la cantidad de partidas con y sin handicap
print('con',df[df.handicap>0].groupby('handicap').handicap.count().sum()*100/total)
print('sin',df[df.handicap==0.0].groupby('handicap').handicap.count().sum()*100/total)
# Prueba de que solo existem 3 tipos de salidas
df2 = df['outcome'].apply(lambda x: 'Resign' if 'Resign'in x else ('Time' if 'Time' in x else x))
df2 = df2[(df2!='Resign') & (df2!='Time')]
df2 = df2.apply(lambda x: 'Points' if 'W+' in x else ('Points' if 'B+' in x else x))
print(df2[df2!='Points']) # esta vacia, solo hay 3 tipos de outputs

#%%
print('porcentaje de partidas con handicap en base sin filtrar', df.handicap[df.handicap>0].shape[0]*100/total)
print('porcentaje de partidas con komi 0.5',df[df.komi==0.5].shape[0]*100/total)
print('porcentaje de partidas con komi 0.5',df0.shape[0]*100/total)
# me quedo solo con el año para asi puedo hacer histograma
df['date']=df['started'].apply(lambda x: x.split()[0][:4])
df0['date']=df0['started'].apply(lambda x: x.split()[0][:4])
print(df0.date.tail)
# Hist partidas por año
#%%
###############################################################################
###############################  date  #######################################
###############################################################################
x = df.groupby('date').date.count().index.tolist()
y = df.groupby('date').date.count().tolist()
x0 = df0.groupby('date').date.count().index.tolist()
y0 = df0.groupby('date').date.count().tolist()
fig, ax = plt.subplots()
ax.bar(x, height=y, edgecolor='black',color='steelblue', label='Complete data base')
#ax.bar(x0, height=y0, edgecolor='black',color='firebrick', label='Filtered only Komi=0.5')
ax.set_yscale("log")
ax.legend()
#labels = [1,10,100,1000,10000,100000,1000000]
#ax.set_yticks(labels, [r' $10^{0}$', r' $10^{1}$', r' $10^{2}$', r'$10^{3}$', r'$10^{4}$', r'$10^{5}$', r'$10^{6}$'])
#ax.get_yaxis().set_major_formatter(ScalarFormatter())
#plt.tight_layout()
ax.minorticks_on()
ax.set_ylabel("Number of games")
plt.xticks( rotation='vertical')
fig.savefig(f'./{name}_date.pdf')
'''
#fig = df.groupby('date').date.count().plot(kind='bar')
x = df.groupby('date').date.count().index.tolist()
y = df.groupby('date').date.count().tolist()
plt.bar(x, height=y)
#plt.xlabel("Year")
plt.ylabel("Number of games")
plt.xticks( rotation='vertical')
#plt.yticks([1, 1000000])

labels = [1,10,100,1000,10000,100000,1000000]
#plt.setp(ax.get_yminorticklabels(), visible=False) # <--- Hide the minors
#plt.yticks(labels, [r' $10^{0}$', r' $10^{1}$', r' $10^{2}$', r'$10^{3}$', r'$10^{4}$', r'$10^{5}$', r'$10^{6}$'])
#plt.yscale('log')

plt.savefig('./date.pdf')
'''
###############################################################################
###############################  jugadores  ####################################
###############################################################################

# Cuantas partidas gano el jugador negro
CountBlackWin = df.groupby('black_win').black_win.count()
#%%
# Hist cantidad de partidas por jugador
#Cambiar la escala de x. mostrar cada 50 bins o algo asi
dfplayer = pd.concat([df.white, df.black], ignore_index=True)
dfplayer.value_counts().hist(ax=ax,bins=50)

print(dfplayer.nunique())
figJ, ax = plt.subplots()

'''
dfplayer0 = pd.concat([df0.white, df0.black], ignore_index=True)
dfplayer0.value_counts().hist(ax=ax,bins=50)
'''
ax.set_yscale('log')
#ax.tick_params(axis='x', pad=50)
#plt.xticks(np.arange(0, 25000, 5000))
#ax.set_xscale('log') # queda muy mal
#fig = plt.gcf()
max = dfplayer.value_counts().max()
min = dfplayer.value_counts().min()
diff = max - min
step = 100
bins = []
y = 0
bins.append(y)
for i in range(int(diff/step) + 1):
    y += step
    bins.append(int(y))
'''
max0 = dfplayer0.value_counts().max()
min0 = dfplayer0.value_counts().min()
diff0 = max0 - min0
bins0 = []
y0 = 0
bins0.append(y0)
for i in range(int(diff0/step) + 1):
    y0 += step
    bins0.append(int(y0))
'''
x = dfplayer.value_counts().value_counts(bins=bins).index.mid.tolist()
y = dfplayer.value_counts().value_counts(bins=bins).tolist()
#x0 = dfplayer0.value_counts().value_counts(bins=bins).index.mid.tolist()
#y0 = dfplayer0.value_counts().value_counts(bins=bins).tolist()
for i in range(len(x)):
    x[i] = int(round(x[i]))

x_ = []
x_ticks = []

fig, ax = plt.subplots(1,1)
plt.figure(0)
plt.bar(x, height=y, width=100, edgecolor='black',color='steelblue')
#plt.bar(x0, height=y0, width=100, edgecolor='black',color='firebrick')
x_ticks = np.arange(0, max, 2000)
plt.xticks(x_ticks)
plt.xlim(0,12000)
plt.xlabel("Number of games")
plt.ylabel("Number of players")
plt.yscale('log')
ax.set_xlabel('')
#plt.show()
#plt.tight_layout()
plt.savefig(f'./{name}_jugadores.pdf')

###############################################################################
###############################  komi  ####################################
###############################################################################
# Hist de valor de Komi
figK, ax = plt.subplots()
df.groupby('komi').komi.count().plot(kind='bar', rot=0, edgecolor='black',color='steelblue')
#df0.groupby('komi').komi.count().plot(kind='bar', rot=0, edgecolor='black',color='firebrick')
ax.set_yscale('log')
ax.set_xlabel('')
figK.savefig(f'./{name}_komi.pdf')

###############################################################################
###############################  handicap  ####################################
###############################################################################
# Hist de valor de handicap, sin log mejor
figH, ax = plt.subplots()
df.groupby('handicap').handicap.count().plot(kind='bar', rot=0, edgecolor='black',color='steelblue', label='Complete data base')
#df0.groupby('handicap').handicap.count().plot(kind='bar', rot=0, edgecolor='black',color='firebrick', label='Filtered only Komi=0.5')
ax.set_yscale('log')
ax.legend()
# Cantidad de partidas con handicap y sin
figH.savefig(f'./{name}_handicap.pdf')
#%%

###############################################################################
###############################  outcomes  ####################################
###############################################################################
# Cantidad de Partidas por tipo de ganada
df['output'] = df['outcome'].apply(lambda x: 'Resign' if 'Resign'in x else ('Time' if 'Time' in x else 'Points'))
df0['output'] = df0['outcome'].apply(lambda x: 'Resign' if 'Resign'in x else ('Time' if 'Time' in x else 'Points'))

figO, ax = plt.subplots()
df.groupby('output').output.count().plot(kind='bar', edgecolor='black',color='steelblue', label='Complete database')
#df0.groupby('output').output.count().plot(kind='bar', edgecolor='black',color='firebrick', label='Filtered only Komi=0.5')
y = df.groupby('output').output.count().tolist()
for index, value in enumerate(y):
    print(index, value)
    plt.text(index-0.17, value+10000, str(value))
labels = ['Points', 'Resign', 'Time']
ax.set_xticklabels(labels, rotation=0, ha='center')
ax.set_yscale('log')
ax.set_xlabel('')
ax.legend()
#labels = [1,10,100,1000,10000,100000,1000000]
#ax.set_yticks(labels, [r' $10^{0}$', r' $10^{1}$', r' $10^{2}$', r'$10^{3}$', r'$10^{4}$', r'$10^{5}$', r'$10^{6}$'])
#ax.get_yaxis().set_major_formatter(ScalarFormatter())
#plt.tight_layout()
ax.minorticks_on()
figO.savefig(f'./{name}_outcomes.pdf')
#%%
