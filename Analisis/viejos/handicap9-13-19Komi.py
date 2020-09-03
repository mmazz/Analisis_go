#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 10:32:51 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
#
import matplotlib.pyplot as plt


##########
#import sys
#sys.path.append('../software/trueskill.py/')
import pandas as pd
#import ablr # analytic-bayesian-linear-regression own package
import numpy as np

df = pd.read_csv('/home/mati/Storage/Tesis/AnalisisGo-Tesis/DatosPurificados/summary_filtered_handicapPositive.csv')
csv = 'tsh_komi_multiJugadorMu0-Beta0'
tsh_all_ogs = pd.read_csv(f'/home/mati/Storage/Tesis/AnalisisGo-Tesis/Analisis/{csv}.csv')
#%%

skill9 = [tsh_all_ogs[(df.handicap==i)&(df.width==9)].iloc[-1].h_mean for i in range(2,6)]
sigma9 = [tsh_all_ogs[(df.handicap==i)&(df.width==9)].iloc[-1].h_std for i in range(2,6)]
NumeroPartidas9 = []
for i in range(2,6):
    NumeroPartidas9.append(df[(df.handicap==i)&(df.width==9)].handicap.value_counts().iloc[0])

skill13= [tsh_all_ogs[(df.handicap==i)&(df.width==13)].iloc[-1].h_mean for i in range(2,8)]
sigma13 = [tsh_all_ogs[(df.handicap==i)&(df.width==13)].iloc[-1].h_std for i in range(2,8)]
NumeroPartidas13 = []
for i in range(2,8):
    NumeroPartidas13.append(df[(df.handicap==i)&(df.width==13)].handicap.value_counts().iloc[0])

skill19 = [tsh_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_mean for i in range(2,10)]
sigma19 = [tsh_all_ogs[(df.handicap==i)&(df.width==19)].iloc[-1].h_std for i in range(2,10)]
NumeroPartidas19 = []
for i in range(2,10):
    NumeroPartidas19.append(df[(df.handicap==i)&(df.width==19)].handicap.value_counts().iloc[0])

handicap9 = list(range(2,6))
handicap13 = list(range(2,8))
handicap19 = list(range(2,10))
#%%

#plt.plot(skill19_ttt);plt.plot(skill19)


width= [9,13,19]
handicaps = [handicap9,handicap13,handicap19]
skills = [skill9,skill13,skill19]
sigmas = [sigma9,sigma13,sigma19]
NumeroPartidas = [NumeroPartidas9,NumeroPartidas13,NumeroPartidas19]
FitHarcodeado = [5,8,8]
x = [1,2,3,4]
y = [3,5,7,10] # 10, not 9, so the fit isn't perfect

coef = np.polyfit(x,y,1)
poly1d_fn = np.poly1d(coef)
# poly1d_fn is now a function which takes in x and returns an estimate for y

plt.plot(x,y, 'yo', x, poly1d_fn(x), '--k')
plt.xlim(0, 5)
for j in range(3):
    for i in range(len(handicaps[j])):
        plt.figure(j)
        plt.plot([handicaps[j][i], handicaps[j][i]], [skills[j][i]+2*sigmas[j][i],
        skills[j][i]-2*sigmas[j][i]], linewidth=0.5, color='grey')
        plt.plot([handicaps[j][i], handicaps[j][i]],[ skills[j][i]+sigmas[j][i],
        skills[j][i]-sigmas[j][i]], linewidth=1, color='black')
        plt.scatter(handicaps[j][i], skills[j][i], label=f'H9- #Partidas={NumeroPartidas[j][i]}')
        plt.legend()
    """
    X_vec = 0
    t = 0
    Phi = 0
    beta = 0
    alpha = 10**(-30) # prior precision
    beta = 1/np.mean(sigmas[j]) # Noise of target value

    t = skills[j]
    X_vec = np.array(handicaps[j]).reshape(-1, 1)
    Phi = ablr.linear.phi(X_vec , ablr.linear.identity_basis_function)


    fit_mu, fit_sigma = ablr.linear.posterior(alpha,beta,t,Phi)
    plt.plot([min(handicaps[j]),max(handicaps[j])],[fit_mu[0]+fit_mu[1]*2,fit_mu[0]+fit_mu[1]*FitHarcodeado[j]],color="black")
    # END: baysian linear regression
    print(fit_mu, fit_sigma )
    """
###

    plt.xticks(fontsize=12) # rotation=90
    plt.yticks(fontsize=12) # rotation=90

    plt.title(rf"{width[j]}X{width[j]}", fontsize=16 )
    plt.xlabel("Handicap", fontsize=16 )
    plt.ylabel("Skill", fontsize=16 )

    plt.savefig("/home/mati/Storage/Tesis/AnalisisGo-Tesis/pdf/"+csv+'-'+str(width[j])+".pdf",pad_inches =0,transparent =True,frameon=True)
    bash_cmd = "pdfcrop --margins '0 0 0 0' pdf/{0}.pdf pdf/{0}.pdf".format(csv+'-'+str(width[j]))
    #os.system(bash_cmd)
