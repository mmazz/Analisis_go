#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:47:13 2020

@author: mati
"""
import numpy as np
import matplotlib.pyplot as plt
import os
name = os.path.basename(__file__).split(".py")[0]

mui = 35
muj = 30
sigma = 25/3
beta = 25/6
leng = 1000
si = np.linspace(-mui, 3*mui, leng)
pi = np.linspace(-mui, 3*mui, leng)
pj = np.linspace(-muj, 3*muj, leng)

Nsi = np.zeros(leng)
Npi_team = np.zeros(leng)
Npj_team = np.zeros(leng)

# matriz de rendimientos y la de team
Matrix_rend = np.zeros((leng, leng))
Matrix_team = np.zeros((leng, leng))


def gaus(x, mu, sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


for i in range(len(pi)):
    Nsi[i] = gaus(si[i], mui, sigma)
    Npi_team[i] = gaus(pi[i], mui, np.sqrt(beta**2 + sigma**2))
    Npj_team[i] = gaus(pj[i], muj, np.sqrt(beta**2 + sigma**2))

# fila columna. Las filas van para los pj
# para cada s_i multiplico con p_i
# la distribucion de habilidad esta pesada por el valor de la distribucion  de
# rendimiento con la media de dicho valor de habilidad

for i in range(len(pi)):
    for j in range(len(pi)):
        a = Nsi[j]*gaus(pi[j], si[i], beta)# el valor de Nsi[j] corresponde al si[j]
        b = Npi_team[i]*Npj_team[j]
        if a > 1e-05:
            Matrix_rend[j][i] = a
        if b > 1e-05:
            Matrix_team[i][j] = b


plt.figure(0)
minlim = int(2*leng/6)
maxlim = int(4*leng/6)
z_min, z_max = -1*abs(Matrix_rend).max(), abs(Matrix_rend).max()
plt.xlim(pi[minlim]-10, pi[maxlim]+10)
plt.ylim(pi[minlim]-10, pi[maxlim]+10)
#plt.pcolor(si,pi,Matrix, cmap='RdBu', vmin=z_min, vmax=z_max, rasterized=True)
levels = np.linspace(0, 0.005, 6)
img = plt.contourf(si, si, Matrix_rend, levels=levels, cmap='Blues')
plt.colorbar(img)
plt.contour(si, si, Matrix_rend, levels=levels, linewidths=0.5, cmap='bone_r', vmin=z_min, vmax=z_max)
#plt.pcolor(si,pi,Matrix, cmap='RdBu', vmin=z_min, vmax=z_max, rasterized=True)
#plt.plot(si, si, c='black', linewidth=1, linestyle='--')
#plt.text(pi[maxlim]-9*sigma/6, pi[maxlim]-8, '$p_i=s_i$')

plt.hlines(mui+5, -100, 100, colors='firebrick', linewidth=2, linestyles='solid')
plt.axvline(x=mui, c='grey', linewidth=0.5, linestyle='--')
plt.hlines(mui, -100, 100, colors='grey', linewidth=0.5, linestyles='dashed')

plt.xticks(ticks=[mui], labels=[r'$\mu_i$'])
plt.yticks(ticks=[mui, mui+5], labels=[r'$\mu_i$', r'$p_i$'])
plt.xlabel(r'Skill $\ s_i$')
plt.ylabel(r'Performance $\ p_i$')
#plt.fill_between(pi, 100000+pi, pi, color='firebrick', alpha=0.3)
plt.xlim(pi[minlim]+5, pi[maxlim]-5)
plt.ylim(pi[minlim]+8, pi[maxlim]-7)
plt.savefig(f'./{name}.pdf')


plt.figure(1)

minlim = int(2*leng/6)
maxlim = int(4*leng/6)
z_min, z_max = -abs(Matrix_team).max(), abs(Matrix_team).max()
#plt.pcolor(si,pj,Matrix2, cmap='RdBu', vmin=z_min, vmax=z_max, rasterized=True)
levels = np.linspace(0, 0.002, 6)
img = plt.contourf(pi, pj, Matrix_team, levels=levels, cmap='Blues')
plt.colorbar(img)
plt.contour(pi, pj, Matrix_team, levels=levels, linewidths=0.5, cmap='bone_r', vmin=z_min, vmax=z_max, zorder=5)
plt.axvline(x=mui, c='grey', linewidth=0.5, linestyle='--')
plt.hlines(muj, -100, 100, colors='grey', linewidth=0.5, linestyles='dashed')
plt.xticks(ticks=[mui], labels=[r'$s_i$'])
plt.yticks(ticks=[muj], labels=[r'$s_j$'])
plt.text(pi[maxlim]-2*sigma+1, pi[maxlim]-18, '$t_e= p_i+p_j =c$')
plt.xlabel('Performance $p_i$')
plt.ylabel('Performance $p_j$')
#plt.fill_between(pi, 100000+pi, pi, color='firebrick', alpha=0.3, zorder=15)
plt.plot(pi, pi, c='black', linewidth=1, linestyle='--')
plt.xlim(pi[minlim]+3, pi[maxlim]-3)
plt.ylim(pi[minlim]+3, pi[maxlim]-13)

plt.savefig(f'./{name}_team.pdf')
