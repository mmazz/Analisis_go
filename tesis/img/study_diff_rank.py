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

# Posteriors finales de cada jugador
#df_ts_h = pd.read_csv('./Datos/TrainingSet_diffRank_TS.csv')
df_TTT_h = pd.read_csv('./TrainingSet_diffRank_TTT.csv')
# Partidas para estimar
df = pd.read_csv('./Datos/StudySet_diffRank.csv')
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


#h_values = [0.028356070825896893, 0.3124751417972205, 0.6923921212654971, 0.6964922495791248, 1.054999313361491, 1.270888901519803, 1.3959710106638124, 1.6174663945338004, 1.9054016143602006, 2.3054016143602006]
def cdf(x, mu, sigma):
    z = -(x - mu) / (sigma * sqrt2)
    return (0.5 * erfc(z))


def erfc(x):
    #"""(http://bit.ly/zOLqbc)"""
    z = abs(x)
    t = 1.0 / (1.0 + z / 2.0)
    a = -0.82215223 + t * 0.17087277; b = 1.48851587 + t * a
    c = -1.13520398 + t * b; d = 0.27886807 + t * c; e = -0.18628806 + t * d
    f = 0.09678418 + t * e; g = 0.37409196 + t * f; h = 1.00002368 + t * g
    r = t * math.exp(-z * z - 1.26551223 + t * h)
    return r if not(x<0) else 2.0 - r


def h_value(black_win, w_mean, b_mean, w_std, b_std, handicap=0):
    std = math.sqrt(2*beta**2 + w_std**2 + b_std**2 + h_std[int(handicap)-1]**2)
    diff = w_mean - (b_mean + h_values[int(handicap)-1])
    # proba = NormalDist(mu=diff, sigma=std).cdf(0)*100  # tienen velocidades parecidas
    proba = cdf(0, diff, std)*100
    return proba

player_study = []
print('Partidas ganadas por negro:', df.black_win.sum(), ' de', df.black_win.shape[0])
# Nombres de los jugadores a estimar
for i in df.index:
    player_study.append(df.loc[i].white)
    player_study.append(df.loc[i].black)

print("Partidas seleccioandas", df.shape[0], " Jugadores seleccionados ", len(player_study))

players_ttt = {}
players_pop = []

for i in player_study:
    #print(df_TTT_h[(df_TTT_h.white == i)|(df_TTT_h.black == i)].iloc[-1])
    df_temporal = df_TTT_h[(df_TTT_h.white == i) | (df_TTT_h.black == i)]
    if df_temporal.shape[0] != 0:
        df_temporal = df_temporal.iloc[-1]
    #print(df_temporal.white)
        if df_temporal.white == i:
            #print('white')
            mean = df_temporal['w_mean']
            std = df_temporal['w_std']
            players_ttt[i] = [mean, std]
        elif df_temporal.black == i:
            #print('black')
            mean = df_temporal['b_mean']
            std = df_temporal['b_std']
            players_ttt[i] = [mean, std]
    else:
        print('no', i)
        # por si justo ese jugador no esta lo saco
        players_pop.append(i)
for i in players_pop:
    player_study = [s for s in player_study if s != i]

Predichos = 0
count = 0
proba = []
black_wins = []
mayor_handicap = 0
menor_handicap = 0
cero_handicap = 0
mayor_handicap_win = 0
menor_handicap_win = 0
cero_handicap_win = 0
# df son las 100 partidas
for i in df.index:
    player1 = df.loc[i].white
    player2 = df.loc[i].black
    if (player1 in player_study) and (player2 in player_study):
        count += 1
        player1_mean = players_ttt[player1][0]
        player2_mean = players_ttt[player2][0]
        player1_std = players_ttt[player1][1]
        player2_std = players_ttt[player2][1]
        player1_rank = int(df.loc[i].whiteRank)
        player2_rank = int(df.loc[i].blackRank)
        handicap = int(df.loc[i].handicap)
        diff = player1_mean - (player2_mean + h_values[handicap])
        diff_rank = player2_rank - (player1_rank + handicap)
        black_win = df.loc[i].black_win
        #prob_win = prob_win_H(black_win, player1_mean, player2_mean,
        #                      player1_std, player2_std, handicap)
        prob_win = h_value(black_win, player1_mean, player2_mean, player1_std, player2_std, handicap)
        proba.append(prob_win)
        if black_win == 1:
            black_wins.append(prob_win)
        if (diff > 0) and (black_win == 0):
            Predichos += 1
        if (diff < 0) and (black_win == 1):
            Predichos += 1

print(" ")
if mayor_handicap != 0:
    print("Se le dio mas handicap", mayor_handicap, mayor_handicap_win, mayor_handicap_win*100/mayor_handicap)
if menor_handicap != 0:
    print("Se le dio menos handicap", menor_handicap, menor_handicap_win, menor_handicap_win*100/menor_handicap)
if cero_handicap != 0:
    print("Se le dio bien handicap", cero_handicap, cero_handicap_win, cero_handicap_win*100/cero_handicap)
#plt.style.use('fivethirtyeight')
#bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85,
#        90, 95, 100]
#bins = [2.5, 7.5,  12.5,  17.5,  22.5,  27.5,  32.5,
#        37.5,  42.5, 47.5, 52.5,  57.5,  62.5,  67.5,  72.5,
#        77.5,  82.5,  87.5,  92.5,  97.5, ]
bins = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]
values, index, _ = plt.hist(proba, bins=bins, edgecolor='black', color='steelblue', label='Total games')
values2, index2, __ = plt.hist(black_wins, bins=bins, edgecolor='black', color='firebrick', label='Black wins')

Probability = values2*100/values
count_bis = 0
for i in range(len(values)):
    count_bis+=1
    if round(Probability[i], 1) >= 0:
        if count_bis%2 == 0:
            plt.text(index[i]+1, values2[i]+0.5, str(round(Probability[i], 1))+'%', color='y')
        else:
            plt.text(index[i]+1, values2[i]-0.5, str(round(Probability[i], 1))+'%', color='y')

ticks = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
plt.xticks(ticks, ticks)
plt.xlabel('Probability black wins')
plt.ylabel("Number of games")
plt.legend()
#plt.show()
plt.savefig(f'./{name}.pdf')
#x = range(0, len(proba))
#plt.scatter(x, proba)
#plt.show()
Preds_correctas_TTT = round(Predichos*100/count, 2)

print("Partidas tomadas: ", count)
print(f'Predicciones correctas TTT: {Preds_correctas_TTT}%')
