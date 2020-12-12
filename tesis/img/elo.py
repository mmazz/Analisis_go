#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 17:18:12 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

mui= 35
muj=30
sigma = 25/6
leng = 1000
pi = np.linspace(-mui,3*mui,leng)
pj = np.linspace(-muj,3*muj,leng)
Ni = np.zeros(leng)
Nj = np.zeros(leng)
Dij = np.zeros(leng)
Matrix = np.zeros((leng, leng))


def gaus(x,mu,sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y

for i in range(len(pi)):
    Ni[i] = gaus(pi[i],mui,sigma)
    Nj[i] = gaus(pj[i],muj,sigma)

# fila columna. Las filas van para los pj
for i in range(len(pi)):
    for j in range(len(pi)):
        Matrix[i][j] = Ni[j]*Nj[i]

# Prueba que todas las lineas verticals y horizobntales son gaussians
linea = np.zeros(leng)
for j in range(len(pi)):
    linea[j] = Ni[500]*Nj[j]

#%%
plt.figure(0)
minlim = int(2*leng/6)
maxlim =  int(4*leng/6)
z_min, z_max = -abs(Matrix).max(), abs(Matrix).max()
#plt.pcolor(pi,pj,Matrix, cmap='RdBu', vmin=z_min, vmax=z_max, rasterized=True)
plt.contourf(pi,pj,Matrix, 5, cmap='Blues')
plt.contour(pi,pj,Matrix, 5, linewidths=0.5, cmap='bone_r', vmin=z_min, vmax=z_max)
plt.axvline(x=mui,c='grey',linewidth=0.5,linestyle='--')
plt.hlines(muj,-100,100,colors='grey',linewidth=0.5,linestyles='dashed')
plt.xticks(ticks=[mui],labels=[r'$s_i$'])
plt.yticks(ticks=[muj],labels=[r'$s_j$'])
plt.xlabel('Performance $p_i$')
plt.ylabel('Performance $p_j$')

plt.plot(pi,pi,c='black',linewidth=1,linestyle='--')
plt.text(6.5*pi[maxlim]/10+3,4.5*pi[maxlim]/10-3,r'Win $i$')
plt.text(5*pi[maxlim]/10-2,6*pi[maxlim]/10+2,r'Win $j$')
plt.text(pi[maxlim]-20*sigma/6,pi[maxlim]-17,'$p_i=p_j$')
plt.xlim(pi[minlim]+8,pi[maxlim]-8)
plt.ylim(pi[minlim]+5,pi[maxlim]-15)

plt.savefig(f'./{name}_diff.pdf')
#%%


#%%
plt.figure(1)
for i in range(len(pi)):
    Dij[i] = gaus(pi[i],mui-muj,2*sigma)

dif = mui-muj
plt.plot(pi,Dij,c='steelblue',linewidth=1,linestyle='--')
plt.fill_between(pi[:251],Dij[:251],facecolor='steelblue', alpha=0.5)
plt.fill_between(pi[250:],Dij[250:],facecolor='grey', alpha=0.3)
plt.axvline(x=dif,c='grey',linewidth=0.5,linestyle='--')
plt.xticks(ticks=[0,dif],labels=[0,r'$(s_i-s_j)$'])
plt.text(dif+5,0.005,r'Win $i$')
plt.text(dif-13,0.005,r'Win $j$')
plt.xlabel('$d_{ij}$')
plt.ylabel('Denisity')
plt.xlim(-30,40)
plt.ylim(0,0.05)

plt.savefig(f'./{name}_diff_gauss.pdf')
