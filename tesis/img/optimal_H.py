#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
black_win es 1 si gano el negro.
"""
import pandas as pd
from statistics import NormalDist
import math
import os
name = os.path.basename(__file__).split(".py")[0]


df_TTT_h = pd.read_csv('./TTT_H_uno.csv')
print(df_TTT_h.black_win.sum()*100/df_TTT_h.shape[0])

handicaps = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
handicaps_color = [0, -1, -2, -3, -4, -5, -6, -7, -8]
h_values = [None] * len(handicaps)
h_values_color = [None] * len(handicaps_color)
#beta = 1.0/(0.21844648724*1.011657753913105)
#h_std = 0.298
beta = 4.45289
h_std = 0.13
sqrt2 = math.sqrt(2)
# index 0 para handicap 1, index 1 para handicap 2 y asi
for i in range(len(handicaps)):
    #h_values[i] = 0.9976 * handicaps[i] - 0.5593# - 0.067
    h_values[i] = 1.00103 * handicaps[i] - 0.6788 # - 0.067
for i in range(len(handicaps_color)):
    h_values_color[i] = 1.00103 * handicaps_color[i] - 0.6788  # - 0.067


#h_values = [0.08604661124825415, 1.3449424858082308, 2.2963710218985667, 3.5780375856054145, 4.495241957738279, 5.367722600128796, 6.4026781916377224, 7.0226838161250935, 8.127094973490343, 9.127094973490343]
h_std = [0.008046329946480087, 0.015502314322638268, 0.019893728722348326, 0.03434667031891241, 0.06067102656362156, 0.0645205360018915, 0.319566591380724, 0.5155001566669764, 0.5155001566669764, 0.5155001566669764, 0.5155001566669764]

h_std_color = 0.52


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




def h_value(w_mean, b_mean, w_std, b_std, handicap):
    # el 10 lo pongo para no usar, demasiada diff
    #std = math.sqrt(2*beta**2 + w_std**2 + b_std**2 + h_std**2)
    h_probs = []
    for i in range(len(handicaps)):
        diff = w_mean - (b_mean + h_values[i])
        std = math.sqrt(2*beta**2 + w_std**2 + b_std**2 + h_std[i]**2)
        #proba = NormalDist(mu=diff, sigma=std).cdf(0)*100 # tienen velocidades parecidas
        proba = cdf(0, diff, std)*100
        h_probs.append(proba)
        if int(handicaps[i]) == int(handicap):
            proba_real = round(proba, 2)
    index, prob = min(enumerate(h_probs), key=lambda x: abs(x[1]-50.0))
    prob = round(prob, 2)
    h = int(handicaps[index])
    if (h == 1) & (prob >= 54.0):
        h_probs_color = []
        for i in range(len(handicaps_color)):
            diff = w_mean - (b_mean + h_values_color[i])
            std = math.sqrt(2*beta**2 + w_std**2 + b_std**2 + h_std_color**2)
            #proba = NormalDist(mu=diff, sigma=std).cdf(0)*100 # tienen velocidades parecidas
            proba = cdf(0, diff, std)*100
            h_probs_color.append(proba)
        index, prob = min(enumerate(h_probs_color), key=lambda x: abs(x[1]-50.0))
        prob = round(prob, 2)
        h = int(handicaps_color[index]-1)
        print(h, prob)

    return h, prob, proba_real


df_TTT_h[['handicap_prediction', 'proba', 'proba_real']] = df_TTT_h.apply(lambda r: h_value(r['w_mean_prior'], r['b_mean_prior'], r['w_std_prior'], r['b_std_prior'], r['handicap']), axis=1, result_type="expand")
df_TTT_h.to_csv("./Datos/TTT_H_analizada.csv", index=True)
