#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error


import os
name = os.path.basename(__file__).split(".py")[0]
#handicaps = [1, 2, 3, 4, 5, 6, 7, 8]
handicaps = [1, 2, 3, 4, 5, 6, 7, 8]
colors = ['red', 'cyan', 'orange', 'green', 'purple', 'blue', 'firebrick', 'magenta', 'firebrick']

df_TTT_h_uno = pd.read_csv('./TTT_H_uno.csv')


'''
#Para no tener que correr el codigo, harcodeo los valores, esto se corre una vez
df_TTT_h = pd.read_csv('./Datos/TTT_H_gamma0.csv')
skills = [df_TTT_h[(df_TTT_h.handicap == i)].iloc[-1].h_mean for i in handicaps]
sigmas = [df_TTT_h[(df_TTT_h.handicap == i)].iloc[-1].h_std for i in handicaps]

NumeroPartidas = []
for i in handicaps:
    NumeroPartidas.append(df_TTT_h[(df_TTT_h.handicap == i)].handicap.value_counts().iloc[0])

print(" ")
print("Skills: ", skills)
print("Sigmas: ", sigmas)
print("Numero de partidas: ", NumeroPartidas)
print(" ")
# con gamma no nulo
skills = [0.022203005264976004, 0.2893374305288187, 0.6562649168321374, 0.6365226783154829, 0.9978880164811206, 1.199509569851498, 1.3064003615926691, 1.5047009245269358]
sigmas = [0.11714289958559244, 0.11744747078306225, 0.11782720022067696, 0.1199450156553534, 0.1204808811251542, 0.12080888407927852, 0.1203091796095326, 0.1359143832480058]
NumeroPartidas = [1077117, 294396, 185496, 62673, 20335, 17690, 739, 306]
'''

# gamma nulo
skills = [0.006735695726989658, 0.2482871015778469, 0.43179793655387216, 0.7016388527207175, 0.8923889745412966, 1.0938399125565, 1.3438859669504186, 1.4485746478199568]
sigmas = [0.0018092015645693516, 0.003486471213244129, 0.004474729025970274, 0.007727358533359064, 0.013645586746330195, 0.014522334780780462, 0.07187699708060441, 0.1158022242566962]
NumeroPartidas = [1077117, 294396, 185496, 62673, 20335, 17690, 739, 306]

h_dist = []
x_dist = []
leng = 1000
for i in range(len(handicaps)):
    normal = np.random.normal(skills[i], sigmas[i], leng)
    for j in range(leng):
        h_dist.append(normal[j])
        x_dist.append(handicaps[i])

coef, V = np.polyfit(x_dist, h_dist, deg=1, cov=True)
da = round(np.sqrt(V[0][0]), 5)
db = round(np.sqrt(V[1][1]), 5)
poly1d_fn = np.poly1d(coef)
print("Fit: ", poly1d_fn)
media = [sum(h_dist)/len(h_dist)]*len(h_dist)
# en realidad no quiero la media... pero como es para calcular el R cuadrado
# al estar dividiendo se cancela el promedio y da lo que quiero.
mse_media = mean_squared_error(h_dist, media)
mse = mean_squared_error(h_dist, poly1d_fn(x_dist))

mse_media = mean_squared_error(h_dist, media)
mse = mean_squared_error(h_dist, poly1d_fn(x_dist))
# es el error cuadratico medio.
# obviamente el polyfit encontro la recta de menor error cuadratico medio
#Rsquare
Rsquare = round((mse_media-mse)/mse_media,2)
# poly1d_fn is now a function which takes in x and returns an estimate for y
plt.figure(1)
#plt.xlim(0, 5)
plt.plot(handicaps, poly1d_fn(handicaps), '--k', color='steelblue', label=f'R$^2$={Rsquare}', zorder=0) #f'Fit: {poly1d_fn}'

for i in range(len(handicaps)):
    plt.plot([handicaps[i], handicaps[i]], [skills[i]+2*sigmas[i],
             skills[i]-2*sigmas[i]], linewidth=0.5, color='black', zorder=5)
    plt.plot([handicaps[i], handicaps[i]], [skills[i]+sigmas[i],
             skills[i]-sigmas[i]], linewidth=2, color='black', zorder=10)
    plt.scatter(handicaps[i], skills[i], color=colors[i], zorder=15)
    #label=f'H{handicaps[i]}- #Partidas={NumeroPartidas[i]}',


plt.legend()
plt.xticks(handicaps, handicaps, fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90
plt.xlabel("Handicap", fontsize=16)
plt.ylabel("Skill", fontsize=16)
#plt.show()
plt.savefig(f'./{name}.pdf')
print('Mu handicap 2: ',skills[0],' Mu handicap 3: ',skills[1], ' Diff: ',skills[1]-skills[0])

############################################################################
############################### FIT UNO ############################
############################################################################

handicaps = [1, 2, 3, 4, 5, 6, 7, 8,9]
skills = [df_TTT_h_uno[(df_TTT_h_uno.handicap == i)].iloc[-1].h_mean for i in handicaps]
sigmas = [df_TTT_h_uno[(df_TTT_h_uno.handicap == i)].iloc[-1].h_std for i in handicaps]
print('handicaps', skills)
print('sigmas', sigmas)
NumeroPartidas = []
for i in handicaps:
    NumeroPartidas.append(df_TTT_h_uno[(df_TTT_h_uno.handicap == i)].handicap.value_counts().iloc[0])


# no le estoy mandando el error en y....

h_dist = []
x_dist = []
leng = 1000
for i in range(len(handicaps)-1):
    normal = np.random.normal(skills[i], sigmas[i], leng)
    for j in range(leng):
        h_dist.append(normal[j])
        x_dist.append(handicaps[i])

print('std dev', np.std(h_dist))


coef, V = np.polyfit(x_dist, h_dist, deg=1, cov=True)
da = round(np.sqrt(V[0][0]),5)
db = round(np.sqrt(V[1][1]),5)
print("x_1: {} +/- {}".format(round(coef[0],5), da))
print("x_2: {} +/- {} ".format(round(coef[1],5), db))

poly1d_fn = np.poly1d(coef)
print("Fit: ", poly1d_fn)
# poly1d_fn is now a function which takes in x and returns an estimate for y

fig, ax = plt.subplots(1, 2, gridspec_kw={
                       'width_ratios': [2,1],
                       'height_ratios': [1]})

ax1 = ax[0]
ax2 = ax[1]

print('sigma handicap promedio', sum(sigmas)/len(sigmas))
for i in range(len(handicaps)):
    ax1.plot([handicaps[i], handicaps[i]], [skills[i]+2*sigmas[i],
             skills[i]-2*sigmas[i]], linewidth=0.5, color='black',zorder=0)
    ax1.plot([handicaps[i], handicaps[i]], [skills[i]+sigmas[i],
             skills[i]-sigmas[i]], linewidth=2, color='black',zorder=5)
    ax1.scatter(handicaps[i], skills[i], color=colors[i], zorder=10)
# calculo el error cuadradito pero de la media
media = [sum(h_dist)/len(h_dist)]*len(h_dist)
# en realidad no quiero la media... pero como es para calcular el R cuadrado
# al estar dividiendo se cancela el promedio y da lo que quiero.
mse_media = mean_squared_error(h_dist, media)
mse = mean_squared_error(h_dist, poly1d_fn(x_dist))

mse_media = mean_squared_error(h_dist, media)
mse = mean_squared_error(h_dist, poly1d_fn(x_dist))
# es el error cuadratico medio.
# obviamente el polyfit encontro la recta de menor error cuadratico medio
#Rsquare
Rsquare = round((mse_media-mse)/mse_media,2)
y = poly1d_fn(handicaps)
# si uso df = len -2 es 3.182, y aca hace t*sqrt(error a)
# por la pagina difce len -1 entonces es 2.776, aca
# aca hace t*std_dev/sqrt(len), parece dar muy chico
ci = 3.182 * np.sqrt(V[0][0])
ci = 2.365 * np.sqrt(V[0][0])#/len(y)

df = len(y) - 2
ax1.plot(handicaps, y, '--k', color='steelblue', label=f'R$^2$={Rsquare}')
#ax1.plot(handicaps, y-db, '--b', color='steelblue', label=f'R$^2$={Rsquare}')
#ax1.plot(handicaps, y-da, '--b', color='steelblue', label=f'R$^2$={Rsquare}')
#ax1.fill_between(handicaps, (y-ci), (y+ci), color='b', alpha=.1, label='95% of confidence')

ax1.legend()
#plt.xticks(fontsize=12) # rotation=90
#plt.yticks(fontsize=12) # rotation=90
ax1.set_xlabel("Handicap", fontsize=16)
ax1.set_ylabel("Skill", fontsize=16)
x_ticks = [0,1,2,3,4,5,6,7,8,9]

ax1.set_xticks(x_ticks)

#ax1.set_ylim(0,55)
NumeroPartidas[i]
x = df_TTT_h_uno.groupby('handicap').handicap.count().index.tolist()
y = df_TTT_h_uno.groupby('handicap').handicap.count().tolist()
#ax2.bar(x[:-1], height=y[:-1], log=True, edgecolor='black')
ax2.bar(x, height=y, log=True, edgecolor='black')

ax2.set_xticks(x_ticks)

fig.savefig(f'./{name}_uno.pdf', dpi=100)

# sin el fit
fig, ax = plt.subplots(1, 2, gridspec_kw={
                       'width_ratios': [2,1],
                       'height_ratios': [1]})

ax1 = ax[0]
ax2 = ax[1]
skills0 = [0.006735695726989658, 0.2482871015778469, 0.43179793655387216, 0.7016388527207175, 0.8923889745412966, 1.0938399125565, 1.3438859669504186, 1.4485746478199568, 1.1]
sigmas0 = [0.0018092015645693516, 0.003486471213244129, 0.004474729025970274, 0.007727358533359064, 0.013645586746330195, 0.014522334780780462, 0.07187699708060441, 0.1158022242566962, 0.04]
print('sigma handicap promedio', sum(sigmas)/len(sigmas))
for i in range(len(handicaps)):
    ax1.plot([handicaps[i], handicaps[i]], [skills[i]+2*sigmas[i],
             skills[i]-2*sigmas[i]], linewidth=0.5, color='black',zorder=0)
    ax1.plot([handicaps[i], handicaps[i]], [skills[i]+sigmas[i],
             skills[i]-sigmas[i]], linewidth=2, color='black',zorder=5)
    ax1.scatter(handicaps[i], skills[i], color=colors[i], zorder=10)
    ax1.plot([handicaps[i], handicaps[i]], [skills0[i]+2*sigmas0[i],
             skills0[i]-2*sigmas0[i]], linewidth=0.5, color='black',zorder=0)
    ax1.plot([handicaps[i], handicaps[i]], [skills0[i]+sigmas0[i],
             skills0[i]-sigmas0[i]], linewidth=2, color='black',zorder=5)
    ax1.scatter(handicaps[i], skills0[i], color='black', zorder=10)
# calculo el error cuadradito pero de la media
media = [sum(h_dist)/len(h_dist)]*len(h_dist)
# en realidad no quiero la media... pero como es para calcular el R cuadrado
# al estar dividiendo se cancela el promedio y da lo que quiero.
mse_media = mean_squared_error(h_dist, media)
mse = mean_squared_error(h_dist, poly1d_fn(x_dist))

mse_media = mean_squared_error(h_dist, media)
mse = mean_squared_error(h_dist, poly1d_fn(x_dist))
# es el error cuadratico medio.
# obviamente el polyfit encontro la recta de menor error cuadratico medio
#Rsquare
Rsquare = round((mse_media-mse)/mse_media,2)
y = poly1d_fn(handicaps)
# si uso df = len -2 es 3.182, y aca hace t*sqrt(error a)
# por la pagina difce len -1 entonces es 2.776, aca
# aca hace t*std_dev/sqrt(len), parece dar muy chico
ci = 3.182 * np.sqrt(V[0][0])
ci = 2.365 * np.sqrt(V[0][0])#/len(y)

df = len(y) - 2

#plt.xticks(fontsize=12) # rotation=90
#plt.yticks(fontsize=12) # rotation=90
ax1.set_xlabel("Handicap", fontsize=16)
ax1.set_ylabel("Skill", fontsize=16)
x_ticks = [0,1,2,3,4,5,6,7,8,9]

ax1.set_xticks(x_ticks)

#ax1.set_ylim(0,55)
NumeroPartidas[i]
print(NumeroPartidas[-1])
x = df_TTT_h_uno.groupby('handicap').handicap.count().index.tolist()
y = df_TTT_h_uno.groupby('handicap').handicap.count().tolist()
#ax2.bar(x[:-1], height=y[:-1], log=True, edgecolor='black')
ax2.bar(x, height=y, log=True, edgecolor='black')

ax2.set_xticks(x_ticks)

fig.savefig(f'./{name}_uno_sinFit.pdf', dpi=100)
############################################################################
############################### Sin FIT ############################
############################################################################
# gamma nulo
handicaps = [1, 2, 3, 4, 5, 6, 7, 8, 9]
colors = ['red', 'cyan', 'orange', 'green', 'purple', 'blue', 'firebrick', 'magenta', 'firebrick']

skills = [0.006735695726989658, 0.2482871015778469, 0.43179793655387216, 0.7016388527207175, 0.8923889745412966, 1.0938399125565, 1.3438859669504186, 1.4485746478199568, 1.1]
sigmas = [0.0018092015645693516, 0.003486471213244129, 0.004474729025970274, 0.007727358533359064, 0.013645586746330195, 0.014522334780780462, 0.07187699708060441, 0.1158022242566962, 0.04]
NumeroPartidas = [1077117, 294396, 185496, 62673, 20335, 17690, 739, 306,1499]

h_dist = []
x_dist = []
leng = 1000
fig, ax = plt.subplots(1, 2, gridspec_kw={
                       'width_ratios': [2,1],
                       'height_ratios': [1]})

ax1 = ax[0]
ax2 = ax[1]
for i in range(len(handicaps)):
    ax1.plot([handicaps[i], handicaps[i]], [skills[i]+2*sigmas[i],
             skills[i]-2*sigmas[i]], linewidth=0.5, color='black',zorder=0)
    ax1.plot([handicaps[i], handicaps[i]], [skills[i]+sigmas[i],
             skills[i]-sigmas[i]], linewidth=2, color='black',zorder=5)
    ax1.scatter(handicaps[i], skills[i], color='black', zorder=10)
    #label=f'H{handicaps[i]}- #Partidas={NumeroPartidas[i]}',
NumeroPartidas[i]
x = df_TTT_h_uno.groupby('handicap').handicap.count().index.tolist()
y = df_TTT_h_uno.groupby('handicap').handicap.count().tolist()
#ax2.bar(x[:-1], height=y[:-1], log=True, edgecolor='black')
ax2.bar(x, height=y, log=True, edgecolor='black')

ax2.set_xticks(x_ticks)
plt.xticks(handicaps, handicaps, fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90
plt.xlabel("Handicap", fontsize=16)
plt.ylabel("Skill", fontsize=16)
#plt.show()
plt.savefig(f'./{name}_sinFit.pdf')
# no aporta nada este grafico
'''
plt.figure(3)

#plt.xlim(0, 5)
colors = ['red','cyan','orange','green','purple']

plt.plot(handicaps[:5], sigmas[:5],marker='*',  markersize=12,linewidth=2., color='steelblue')
plt.legend()
plt.xticks(fontsize=12) # rotation=90
plt.yticks(fontsize=12) # rotation=90
plt.xlabel("Sigma", fontsize=16)
plt.ylabel("Skill", fontsize=16)
plt.savefig('./handicap_fit_uno_sigma.pdf')
'''


'''

# forma de regrtession lineal.
dy = np.array(sigmas)
print('sigmas', sigmas)


def chi_2(params,x,y,sigy):
    m,c=params
    return sum(((y-m*x-c)/sigy)**2)


x = np.array(handicaps)
y = np.array(skills)

data_in = (x, y, dy)
params0 = [1,0]

q = fmin(chi_2, params0, args=data_in)
print(q)
'''
