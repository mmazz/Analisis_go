#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 15:17:41 2020

@author: mati
"""

import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy.special import erf


def gaussian(x, mu, sig):
    return 1./(np.sqrt(2.*np.pi*sig))*np.exp(-np.power(x - mu, 2)/(sig*2.))


mu = 25.5
muWin = 15
sigmaWin = 40
sigma = 5
beta = 5
xSkill = np.linspace(-3*mu, 3*mu, 1000)
dt = xSkill[1]-xSkill[0]


# %% 
mu = 3.5
beta = 1
x = 1.5
P2 = gaussian(xSkill, mu, beta**2)
gaus2 = gaussian(xSkill, -mu, beta**2)
gauscum2 = gaussian(xSkill, -mu-x, beta**2)

# xSkill[500] = 0
# xSkill[533] = 0.5
#xSkill[600] = 1.5
cumorig= np.sum(gaus2[:600]*dt)  # Veo normalizacion
cum2= np.sum(gauscum2[:500]*dt)  # Veo normalizacion
print(cumorig,cum2)



# %% Prueba ELO
P1 = gaussian(xSkill, muWin, beta**2)
P2 = gaussian(xSkill, mu, beta**2)

PDiff = gaussian(xSkill,muWin - mu, 2*beta**2)

plt.plot(xSkill,PDiff)
Cumulative = np.zeros(1000)

for i in range(1,len(PDiff)):
    Cumulative[i] = Cumulative[i-1] + PDiff[i]*dt
    
plt.plot(xSkill,Cumulative) # En cero cae la proba que tiene uno de ganar sobre el otro


for i in range(len(PDiff)):
    if xSkill[i] >= 0:
        indexCumulativeGanador = i
        break
        

ProbaPerderdor = Cumulative[indexCumulativeGanador]
ProbaGanador = 1 - ProbaPerderdor

# %%
SGauss = gaussian(xSkill, mu, sigma**2)
PGauss = gaussian(xSkill, mu, beta**2)
np.sum(SGauss*dt)  # Riemann multiplicar dt!!! Normalizado

P_pi = np.zeros(len(xSkill))
MatrizCon = np.zeros([len(xSkill), len(xSkill)])

# %%
countS = 0
plt.figure(1)
for s in xSkill:  # x = p,  y = s
    MatrizCon[countS, :] = gaussian(xSkill, s, beta**2)\
    * gaussian(s, mu, sigma**2)
    countS += 1
    plt.plot(xSkill, MatrizCon[countS-1, :])
MatrizCon = np.transpose(np.flip(MatrizCon, axis=0))  # x = s y=p
plt.imshow(MatrizCon)

# %%
plt.plot(xSkill, MatrizCon[500, :])
np.sum(MatrizCon*dt**2)  # Veo normalizacion

matrix = np.ones([2, 2])
plt.imshow(matrix[0, :])
plt.plot(xSkill, np.transpose(MatrizCon[:, countS-20]))
plt.plot(xSkill, np.transpose(MatrizCon[countS-20, :]))

np.sum(MatrizCon[countS-30, :])
# %%
# mensaje 4
P_p = np.sum(MatrizCon*dt, axis=1)  # axis=0 suma todas las filas
NormalS = gaussian(xSkill, mu, sigma**2)
NormalP = gaussian(xSkill, mu, beta**2+sigma**2)

plt.figure(2)
plt.plot(xSkill, P_p, 'k', label="mens 4")  # Es el mensaje 4
plt.plot(xSkill, NormalS, '*r', label="Normal(s,sigma)")
plt.plot(xSkill, NormalP, '*b', label="Normal(s,beta)")
plt.legend()

# %%
# mensaje 6??
suma = np.zeros(len(xSkill))

for i in range(len(xSkill)):
    suma[i] = NormalP[i]*dt/(np.sqrt(2)*5) + suma[i-1]

plt.plot(xSkill, suma)
plt.plot(xSkill, NormalP)



# %%
NormalP = gaussian(xSkill, muWin, beta**2+sigmaWin**2)
mensjC = gaussian(xSkill, muWin, sigma**2+beta**2)
plt.plot(xSkill, suma)
# plt.plot(xSkill,mensjC)
plt.plot(xSkill, NormalP*suma)
plt.plot(xSkill, NormalP)
# %%


def cumul(x, mu, sigma):
    return 0.5*(1+erf((x-mu)/(sigma*np.sqrt(2))))


normcum = np.zeros(len(xSkill))


for i in range(len(xSkill)):
    normcum[i] = cumul(xSkill[i], mu, sigma)

plt.plot(xSkill, normcum)
