#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:47:13 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import matplotlib.pyplot as plt


mui = 35
muj = 30
sigma = 25/3
beta = 25/6
leng = 1000
si = np.linspace(-mui, 3*mui, leng)
pi = np.linspace(-mui, 3*mui, leng)
pj = np.linspace(-muj, 3*muj, leng)

Ni = np.zeros(leng)
Nj = np.zeros(leng)

Matrix = np.zeros((leng, leng))
Matrix2 = np.zeros((leng, leng))


def gaus(x, mu, sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


for i in range(len(pi)):
    Ni[i] = gaus(si[i], mui, sigma)
    Nj[i] = gaus(pi[i], muj, sigma)

# fila columna. Las filas van para los pj
# para cada s_i multiplico con p_i
for i in range(len(pi)):
    for j in range(len(pi)):
        a = Ni[j]*gaus(pi[j], si[i], sigma)
        b = Ni[j]*Nj[i]
        if a > 1e-05:
            Matrix[j][i] = a
        if b > 1e-05:
            Matrix2[i][j] = b


#%%
plt.figure(0)
minlim = int(2*leng/6)
maxlim = int(4*leng/6)
z_min, z_max = -1*abs(Matrix).max(), abs(Matrix).max()
plt.xlim(pi[minlim]-10, pi[maxlim]+10)
plt.ylim(pi[minlim]-10, pi[maxlim]+10)
#plt.pcolor(si,pi,Matrix, cmap='RdBu', vmin=z_min, vmax=z_max, rasterized=True)
plt.contourf(si, pi, Matrix, 5, cmap='Blues')
plt.contour(si, pi, Matrix, 5, linewidths=0.5, cmap='bone_r', vmin=z_min, vmax=z_max)
#plt.pcolor(si,pi,Matrix, cmap='RdBu', vmin=z_min, vmax=z_max, rasterized=True)


plt.plot(si, si, c='black', linewidth=1, linestyle='--')
plt.hlines(mui+5, -100, 100, colors='black', linewidth=1.5, linestyles='solid')
plt.xticks(ticks=[mui], labels=[r'$s_i$'])
plt.yticks(ticks=[mui], labels=[r'$p_i$'])
plt.xlabel('Skill')
plt.ylabel('Performance')
plt.text(pi[maxlim]-2*sigma/6, pi[maxlim]-5, '$p_i=s_i$')


plt.savefig(f'./{name}.pdf')



#%%
plt.figure(1)

minlim = int(2*leng/6)
maxlim =  int(4*leng/6)
z_min, z_max = -abs(Matrix).max(), abs(Matrix).max()
#plt.pcolor(si,pj,Matrix2, cmap='RdBu', vmin=z_min, vmax=z_max, rasterized=True)
plt.contourf(si, pi, Matrix2, 5, cmap='Blues')
plt.contour(si,pi,Matrix2, 5, linewidths=0.5,cmap='bone_r', vmin=z_min, vmax=z_max)
plt.axvline(x=mui,c='grey',linewidth=0.5,linestyle='--')
plt.hlines(muj,-100,100,colors='grey',linewidth=0.5,linestyles='dashed')
plt.xticks(ticks=[mui],labels=[r'$s_i$'])
plt.yticks(ticks=[muj],labels=[r'$s_j$'])
plt.text(pi[maxlim]-sigma,pi[maxlim]-10,'$t_e=c$')
plt.xlabel('Performance $p_i$')
plt.ylabel('Performance $p_j$')

plt.plot(pi,pi,c='black',linewidth=1,linestyle='--')


plt.xlim(pi[minlim],pi[maxlim])
plt.ylim(pi[minlim]-10,pi[maxlim])

plt.savefig(f'./{name}_team.pdf')
