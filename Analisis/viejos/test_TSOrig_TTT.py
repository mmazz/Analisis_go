#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 16:26:11 2020

@author: mati
"""

import os
name = os.path.basename(__file__).split(".py")[0]
import pandas as pd
import sys
sys.path.append('/home/mati/Storage/Tesis/AnalisisGo-Tesis/')
import TTT as thM
import trueskill as true
from importlib import reload

reload(thM)
envTrueskill = true.TrueSkill(draw_probability=0)
env = thM.TrueSkill(draw_probability=0)

################### 1 vs 1 ######################

env = thM.TrueSkill(draw_probability=0)
player1 = envTrueskill.Rating(mu=12)
player2 = envTrueskill.Rating(mu=16)
player1, player2 = envTrueskill.rate([(player1,),(player2,)], ranks=[0, 1])
print(player1, player2)
#%%
player1 = [env.Rating(mu=12)]
player2 = [env.Rating(mu=16)]
result = [0, 1]  # team2 wins
game = env.Game([player1, player2], result)
[[player1], [player2]] = game.posterior
print(player1, player2)


composition = [[[1],[3]]]
results = [[0,1]]
playerDic = {1:env.Rating(mu=12),3:env.Rating(mu=16)}
historyM = env.history(composition,results,batch_numbers=None,prior_dict=playerDic)
historyM.through_time(online=True)
print(historyM.posteriors_player())
#%%

################### 2 vs 2 ######################

env = thM.TrueSkill(draw_probability=0)
player1 = envTrueskill.Rating(mu=12)
player2 = envTrueskill.Rating(mu=21)
player3 = envTrueskill.Rating(mu=16)
player4 = envTrueskill.Rating(mu=20)
player1, player2 = envTrueskill.rate([(player1,player2),(player3,player4)], ranks=[0, 1])
print(player1, player2)
#%%
player1 = [env.Rating(mu=12),env.Rating(mu=21)]
player2 = [env.Rating(mu=16),env.Rating(mu=20)]
result = [0, 1]  # team2 wins
game = env.Game([player1, player2], result)
print(game.posterior)
#print(player1, player2)



composition = [[[1,2],[3,4]]]
results = [[0,1]]
playerDic = {1:env.Rating(mu=12),2:env.Rating(mu=21),3:env.Rating(mu=16),4:env.Rating(mu=20)}
historyM = env.history(composition,results,batch_numbers=None,prior_dict=playerDic)
historyM.through_time(online=False)
#%%  Hasta aca dan igual, problema en mas de 2 equipos
################### 1 vs 1 vs 1######################


player1 = envTrueskill.Rating()
player2 = envTrueskill.Rating()
player3 = envTrueskill.Rating()
player1, player2, player3 = envTrueskill.rate([(player1,),(player2,),(player3,)], ranks=[1, 0,1])
print(player1, player2, player3)
# env = thM.TrueSkill(draw_probability=0)
# player1 = [env.Rating(mu=22)]
# player2 = [env.Rating(mu=26)]

# result = [0, 1]  # team2 wins
# game = env.Game([player1, player2], result)
# [[player1], [player2]] = game.posterior
#print(game.posterior)
#%%
result = [0, 1,0]
player1 = [env.Rating()]
player2 = [env.Rating()]
player3 = [env.Rating()]
game = env.Game([player1, player2, player3], result)
[[player1], [player2], [player3]] = game.posterior
print(player1, player2, player3)
