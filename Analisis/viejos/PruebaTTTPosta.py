#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 19:28:45 2020

@author: mati
"""

import os
name = os.path.basename(__file__).split(".py")[0]
import pandas as pd
import sys
sys.path.append('/home/mati/Storage/Tesis/AnalisisGo-Tesis')
#sys.path.append('/home/mmazzanti/AnalisisGo-Tesis')
import src as thM
from importlib import reload
from collections import defaultdict
import pickle

reload(thM)
#%%

df = pd.read_csv('/home/mati/Storage/Tesis/AnalisisGo-Tesis/crawler/KGS_filtered.csv')
#df = pd.read_csv('/home/mmazzanti/AnalisisGo-Tesis/crawler/KGS_filtered_handicapPositive.csv')
# sacar jugadores que jueguen contra ellos mismos.
df=df[:50]

df = df[(~df.white.str.contains('bot',case=False, na=False))&(~df.black.str.contains('bot',case=False, na=False))]
df = df[df.width==19]
df=df[df.white!=df.black]
df['date'] = df['started'].apply(lambda row: row[0:7])
print(df.date[0])
df = df[df.date.str.contains('2007')]
print("Total: ", df.shape)
#df=df[:50]
df.handicap = df.handicap.apply(lambda x: x if x>=2 else 0)
path = '/home/mati/Storage/Tesis/AnalisisGo-Tesis/crawler'
#path = '/home/mmazzanti/AnalisisGo-Tesis/crawler'
#%%
df = df[(df.komi==0.5)|(df.komi==5.5)|(df.komi==6.5)|(df.komi==7.5)]
print("Komis estandar: ", df.shape)
#%%
prior_dict = defaultdict(lambda: thM.Rating(thM.Gaussian(0,25/3), 0, 1/100))
#for h_key in set([(h, s) for h, s in zip(df.handicap, df.width)]):
#    prior_dict[h_key]
for h_key in set([str(h) for h in df.handicap]):
    prior_dict[h_key]
    #%%
results = list(df.black_win.map(lambda x: [1, 0] if x else [0, 1]))
composition = [[[w], [b]] if h < 2 else [[w], [b, str(h)]] for w, b, h, s in zip(df.white, df.black, df.handicap, df.width)]
batch = list(df.date)
count = 0
for i in range(len(batch)-1):
    if batch[i]==batch[i+1]:
        batch[i] = count
    else:
        batch[i] = count
        count += 1
batch[-1] = count
print("Composicion: ", composition[:5])
print("Resultado: ", results[:5])
print(" ")
print('Starting TrueSkill')
historyM = thM.History(composition, results, batch)
#print('TrueSkill', historyM.batches[0].posteriors())
pickle_file = open('./trueSkill.pickle', 'wb')
print('Saving TrueSkill data')
pickle.dump(historyM.learning_curves(), pickle_file)
pickle_file.close()
print('Saving evidence')
evidence={}
for i in range(len(historyM.batches)):
    evidence[i] = historyM.batches[i].evidences

evidence_file = open('./trueSkillEvidence.pickle', 'wb')
pickle.dump(evidence, evidence_file)
evidence_file.close()
print('Done!, starting TTT converge')
step, i = historyM.convergence()
print('TTT converge!')
#print(historyM.batches[0].evidences)
#print(historyM.learning_curves())
pickle_file = open('./TTT.pickle', 'wb')
print('Saving data')
pickle.dump(historyM.learning_curves(), pickle_file)
pickle_file.close()
print('Donde! Saving evidence')
evidence={}
for i in range(len(historyM.batches)):
    evidence[i] = historyM.batches[i].evidences

evidence_file = open('./TTTevidence.pickle', 'wb')
pickle.dump(evidence, evidence_file)
evidence_file.close()
print('Donde!')
