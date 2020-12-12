#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statistics import NormalDist
import math
import os
name = os.path.basename(__file__).split(".py")[0]
leng = 10000

# Posteriors finales de cada jugador
df_TTT_h = pd.read_csv('./TrainingSet_sameRank_TTT.csv')
# Partidas para estimar
df = pd.read_csv('./Datos/StudySet_sameRank.csv')

handicaps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#h_value = 0.542
#h_values = [h_value-1, h_value,  h_value+1,  h_value+2, h_value+3, h_value+4,
#            h_value+5, h_value+6, h_value+7, h_value+8, h_value+9]
h_values = [None] * len(handicaps)
#h_values = []
# index 0 para handicap 1, index 1 para handicap 2 y asi
for i in range(len(handicaps)):
    h_values[i] = 1.00103 * handicaps[i] - 0.6788

beta = 4.45289
sqrt2 = math.sqrt(2)

#h_values = [0.08604661124825415, 1.3449424858082308, 2.2963710218985667, 3.5780375856054145, 4.495241957738279, 5.367722600128796, 6.4026781916377224, 7.0226838161250935, 8.127094973490343, 9.127094973490343]
h_std = [0.008046329946480087, 0.015502314322638268, 0.019893728722348326, 0.03434667031891241, 0.06067102656362156, 0.0645205360018915, 0.319566591380724, 0.5155001566669764, 0.5155001566669764, 0.5155001566669764, 0.5155001566669764]

def h_value(w_mean, b_mean, w_std, b_std):
    std = math.sqrt(2*beta**2 + w_std**2 + b_std**2 + h_std[0]**2)
    diff = w_mean - (b_mean + h_values[0])
    proba = NormalDist(mu=diff, sigma=std).cdf(0)*100  # tienen velocidades parecidas
    return proba


player_study = []
print('Partidas ganadas por negro:', df.black_win.sum(), ' de', df.black_win.shape[0])
# Nombres de los jugadores a estimar, Pueden estar repetidos una vez
for i in df.index:
    player_study.append(df.loc[i].white)
    player_study.append(df.loc[i].black)

print("Partidas seleccioandas", df.shape[0], " Jugadores seleccionados ", len(player_study))
# agarro el ultimo posterior del jugador
players_ttt = {}
players_pop = []

# Recorro jugador por jugador
for i in player_study:
    # me agarro solo las partidas con ese jugador
    df_temporal = df_TTT_h[(df_TTT_h.white == i) | (df_TTT_h.black == i)]
    # Por algun motivo algunos jugadores no aparecen, entonces chequeo
    if df_temporal.shape[0] != 0:
        # agarro la ultima partida
        df_temporal = df_temporal.iloc[-1]
        # me fijo si jugo como blanco o negro
        if df_temporal.white == i:
            # agarro sus posteriors y me quedo con el ultimo
            #print(df_temporal['w_mean'], df_temporal['w_mean'].tolist())
            mean = df_temporal['w_mean']
            std = df_temporal['w_std']
            players_ttt[i] = [mean, std]
        elif df_temporal.black == i:
            mean = df_temporal['b_mean']
            std = df_temporal['b_std']
            players_ttt[i] = [mean, std]
    else:
        print('no', i)
        # me guardo los jugadores que no estan
        players_pop.append(i)
# saco a los jugadores que no estan
for i in players_pop:
    player_study = [s for s in player_study if s != i]
print('sali')

Predichos = 0
count = 0
proba = []
black_wins = []
# df son las 100 partidas
for i in df.index:
    player1 = df.loc[i].white
    player2 = df.loc[i].black
    if (player1 in player_study) and (player2 in player_study):
        #print('entre')
        count += 1
        player1_mean = players_ttt[player1][0]
        player2_mean = players_ttt[player2][0]
        player1_std = players_ttt[player1][1]
        player2_std = players_ttt[player2][1]
        diff = player1_mean - player2_mean
        player1_rank = int(df.loc[i].whiteRank)
        player2_rank = int(df.loc[i].blackRank)
        handicap = int(df.loc[i].handicap)
        diff_rank = player2_rank - player1_rank
        black_win = df.loc[i].black_win
        prob_win = h_value(player1_mean, player2_mean, player1_std, player2_std)
        proba.append(prob_win)
        if black_win == 1:
            black_wins.append(prob_win)
        if (diff > 0) and (black_win == 0):
            Predichos += 1
        if (diff < 0) and (black_win == 1):
            Predichos += 1


#plt.style.use('fivethirtyeight')


#bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
#bins = [0, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 27.5, 30, 32.5, 35,
#        37.5, 40, 42.5, 45, 47.5, 50,52.5, 55, 57.5, 60, 62.5, 65, 67.5, 70, 72.5,
#        75, 77.5, 80, 82.5, 85, 87.5, 90, 92.5, 95, 97.5, 100]

bins = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
#bins = [2.5, 7.5,  12.5,  17.5,  22.5,  27.5,  32.5,
#        37.5,  42.5, 47.5, 52.5,  57.5,  62.5,  67.5,  72.5,
#        77.5,  82.5,  87.5,  92.5,  97.5]


fig, ax = plt.subplots()
values, index, _ = ax.hist(proba, bins=bins, edgecolor='black', color='steelblue', label='Total games')
values2, index2, __ = ax.hist(black_wins, bins=bins, edgecolor='black', color='firebrick', label='Black wins')
Probabilitys = []
for i in range(len(values)):
    if values[i] != 0:
        Probabilitys.append(values2[i]*100/values[i])
    else:
        Probabilitys.append(0)
count_bis = 0
for i in range(len(values)):
    count_bis += 1
    if round(Probabilitys[i], 1) >= 0:
        if count_bis % 2 == 0:
            ax.text(index[i]+1, values2[i]+0.5, str(round(Probabilitys[i], 1))+'%', color='y')
        else:
            ax.text(index[i]+1, values2[i]-0.5, str(round(Probabilitys[i], 1))+'%', color='y')

ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
ax.set_xticks(ticks)

ax.set_xlabel('Probability black wins')
ax.set_ylabel("Number of games")
plt.legend()
plt.savefig(f'./{name}.pdf')
#x = range(0, len(proba))
#plt.scatter(x, proba)
#plt.show()
#Preds_correctas_TTT = round(Predichos*100/count, 2)
#Preds_correctas_TS = round(Predichos_ts*100/count, 2)
#Preds_correctas_lower = round(perdidas_negro*100/count_perdidas_negro, 2)
#Preds_correctas_upper = round(victorias_negro*100/count_victorias_negro, 2)
#print("Partidas tomadas: ", count)
#print(f'Predicciones correctas TTT: {Preds_correctas_TTT}%')
#| Predicciones correctas TS: {Preds_correctas_TS}%')
#print(f'Predicciones correctas en el rango 0 a 30%: {Preds_correctas_lower}% de {count_perdidas_negro}| Predicciones correctas en el rango 70 a 100%: {Preds_correctas_upper}% de {count_victorias_negro}')
#print(f'Predicciones correctas en el rango 45 a 55%: {victorias_negro_equiprob}% de {count_victorias_negro_equiprob}')
