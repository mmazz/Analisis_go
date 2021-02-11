#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 19:56:47 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import matplotlib.pyplot as plt
"""
import sys
sys.path.append('/home/mati/Storage/Tesis/AnalisisGo-Tesis/')
import src as thM
envM = thM.TrueSkill(draw_probability=0)
muBlanco= 45
muNegro = 25
sigmaBlanco = 2.16
sigmaNegro = 8.34
# White win
twM = [envM.Rating(muBlanco,sigmaBlanco)]
tbM = [envM.Rating(muNegro,sigmaNegro),envM.Rating(2,25/6,25/6,0)]
game = envM.Game([twM,tbM], [0, 1])
[[player1], [player2, player3]] = game.posterior
#print(player1,player2)
#TrueSkill.Rating(mu=50.105, sigma=4.126) TrueSkill.Rating(mu=24.577, sigma=8.066)
muBlanco2win = player1.mu
muNegro2lose = player2.mu
sigmaBlanco2win = player1.sigma
sigmaNegro2lose = player2.sigma
# Black Win
twM = [envM.Rating(muBlanco,sigmaBlanco)]
tbM = [envM.Rating(muNegro,sigmaNegro),envM.Rating(2,25/6,25/6,0)]
game = envM.Game([twM,tbM], [1, 0])
[[player1], [player2, player3]] = game.posterior
#print(player1,player2)
#TrueSkill.Rating(mu=33.277, sigma=3.983) TrueSkill.Rating(mu=31.926, sigma=6.800)
muBlanco2lose = player1.mu
muNegro2win = player2.mu
sigmaBlanco2lose = player1.sigma
sigmaNegro2win = player2.sigma
"""
#%%
muBlanco= 45
muBlanco2win = 45.054
muBlanco2lose =  44.245
muNegro = 25
muNegro2lose = 24.197
muNegro2win = 36.259

sigmaBlanco = 2.16
sigmaBlanco2win = 2.152
sigmaBlanco2lose = 2.13
sigmaNegro = 8.34
sigmaNegro2lose = 7.868
sigmaNegro2win = 6.396

#%%
x = np.linspace(-muBlanco,3*muBlanco,1000)

yB = np.linspace(-muBlanco,3*muBlanco,1000)
yB2W = np.linspace(-muBlanco,3*muBlanco,1000)
yB2L = np.linspace(-muBlanco,3*muBlanco,1000)
yN = np.linspace(-muBlanco,3*muBlanco,1000)
yN2L = np.linspace(-muBlanco,3*muBlanco,1000)
yN2W = np.linspace(-muBlanco,3*muBlanco,1000)

def gaus(x,mu,sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y

for i in range(len(x)):
    yB[i] = gaus(x[i],muBlanco,sigmaBlanco)
    yB2W[i] = gaus(x[i],muBlanco2win,sigmaBlanco2win)
    yB2L[i] = gaus(x[i],muBlanco2lose,sigmaBlanco2lose)
    yN[i] = gaus(x[i],muNegro,sigmaNegro)
    yN2L[i] = gaus(x[i],muNegro2lose,sigmaNegro2lose)
    yN2W[i] = gaus(x[i],muNegro2win,sigmaNegro2win)


plt.figure(0)
plt.plot(x,yB,c='firebrick',linewidth=2,linestyle='-', label="Prior Blanco")
plt.plot(x,yB2W,c='firebrick',linewidth=2,linestyle='--', label="Posterior Blanco")
plt.plot(x,yN,c='steelblue',linewidth=2,linestyle='-', label="Prior Negro")
plt.plot(x,yN2L,c='steelblue',linewidth=2,linestyle='--', label="Posterior Negro")
plt.xlabel('Skill')
plt.ylabel('Performance')
plt.xlim(0,60)
plt.legend()
plt.savefig(f'./{name}_black_lose.pdf')


plt.figure(1)
plt.plot(x,yB,c='firebrick',linewidth=2,linestyle='-', label="Prior Blanco")
plt.plot(x,yB2L,c='firebrick',linewidth=2,linestyle='--', label="Posterior Blanco")
plt.plot(x,yN,c='steelblue',linewidth=2,linestyle='-', label="Prior Negro")
plt.plot(x,yN2W,c='steelblue',linewidth=2,linestyle='--', label="Posterior Negro")
plt.xlabel('Skill')
plt.ylabel('Performance')
plt.xlim(0,60)
plt.legend()
plt.savefig(f'./{name}_black_win.pdf')

plt.figure(2)
plt.plot(x,yB,c='firebrick',linewidth=2,linestyle='-', label="Prior Blanco")
plt.plot(x,yN,c='steelblue',linewidth=2,linestyle='-', label="Prior Negro")
plt.xlabel('Skill')
plt.ylabel('Performance')
plt.xlim(0,60)
plt.legend()
plt.savefig(f'./{name}_black_lose_prior.pdf')


plt.figure(3)
plt.plot(x,yB,c='firebrick',linewidth=2,linestyle='-', label="Prior Blanco")
plt.plot(x,yN,c='steelblue',linewidth=2,linestyle='-', label="Prior Negro")
plt.xlabel('Skill')
plt.ylabel('Performance')
plt.xlim(0,60)
plt.legend()
plt.savefig(f'./{name}_black_win_prior.pdf')
