#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from scipy.optimize import curve_fit
# black_win es 1 si gano el negro.
# hago una elipse

### ranking
df_TTT_h = pd.read_csv('./TTT_H_uno.csv')


df_TTT_h = df_TTT_h[['id','white','black','whiteRank','blackRank']]
# Ordeno los jugadores por cantidad de partidas
df_TTT_h =df_TTT_h[df_TTT_h.whiteRank.str.contains('d',case=False, na=False)]
df_TTT_h =df_TTT_h[df_TTT_h.blackRank.str.contains('d',case=False, na=False)]

df_TTT_h['whiteRank'] = df_TTT_h.whiteRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
df_TTT_h['blackRank'] = df_TTT_h.blackRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
#df_TTT_h=df_TTT_h.drop(['blackRank', 'whiteRank'])
df_TTT_h = df_TTT_h[df_TTT_h['whiteRank'].notnull()]
df_TTT_h = df_TTT_h[df_TTT_h['blackRank'].notnull()]

skills_cero = []
population_cero = []
alpha = []

df_TTT_h['Difference'] = df_TTT_h['whiteRank'] - df_TTT_h['blackRank']
#df_TTT_h['Difference'] = df_TTT_h['Difference'].apply(lambda x: np.abs(x))
print(df_TTT_h['Difference'].mean())



asd

#quizas agarrar los jugadores que arrancaron con un dado ranking
player_numb_games = df_TTT_h[['white','black']].stack().value_counts()
fig, ax = plt.subplots()
plt.figure(5)
for n in range(10,2,-1):
    print(n)
    subplayers = player_numb_games[(player_numb_games > 2**n) & (player_numb_games < 2**(n+1))]
    # Lista de jugadores dentro de un rango
    players = []
    for i in subplayers.index:
        players.append(i)
    # unico dataframe con los jugaores de interes en unica columna, con sus respectivas
    # medias y fecha de juego
    df_white = df_TTT_h[['white','whiteRank']][df_TTT_h.white.isin(players)]
    df_black = df_TTT_h[['black','blackRank]][df_TTT_h.black.isin(players)]
    df_white = df_white.rename(columns={"white": "player", "whiteRank": "mean"})
    df_black = df_black.rename(columns={"black": "player", "blackRank": "mean"})
    frames = [df_white, df_black]
    result = pd.concat(frames)
    result.reset_index(drop=True, inplace=True)
    df = pd.concat([result[result.player == p]['mean'].reset_index(drop=True) for p in players], axis=1, ignore_index=True)
    #df = pd.concat([result[col].sort_values().reset_index(drop=True) for col in result], axis=1, ignore_index=True)
    df = df.reset_index(drop=True)
    df = df[:2**n]
    x = df.index.tolist()
    mean = df.mean(axis=1).tolist()
    mean = [int(round(num, 0)) for num in mean]
    plt.plot(x, mean, label=r'{} games'.format(2**n))

    #plt.text(x[-1]+n, mean[-1], r'$\alpha =${}'.format(2**n,"{:.2e}".format(alpha[-1])))
plt.xscale('log')
plt.xlabel("Games played", fontsize=16)
plt.ylabel(r"$\sigma$", fontsize=16)
plt.legend()
#plt.show()
plt.savefig(f'./{name}.pdf')
