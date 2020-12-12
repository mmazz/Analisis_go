#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 17:24:27 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import matplotlib.pyplot as plt

leng = 1000
mu = 30
muL = 25
sigma = 25/3
x = np.linspace(-mu,3*mu,leng)
y = np.linspace(-mu,3*mu,leng)
z = np.zeros(leng)
z2 = np.zeros(leng)
diff = np.zeros(leng)
top =np.ones(leng)
delta=x[1]-x[0]


def gaus(x,mu,sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y

for i in range(len(x)):
    y[i] = gaus(x[i],mu,sigma)
    diff[i] = gaus(x[i],mu-muL,sigma)

for i in range(len(x)):
    if i == 0:
        z[i] =y[i]*delta
    else:
        z[i]=z[i-1] + y[i]*delta

for i in range(len(x)):
    z2[i] = y[i]*z[i]
#%%
plt.figure(0)


plt.plot(x,y,c='steelblue',linewidth=2,linestyle=':',label='Prior')
#x0 = x[:241]
mux = x[500]
cumy = z[362]

plt.text(31,0.005,'Evidence')
plt.fill_between(x,top,z*0.048,facecolor='steelblue', alpha=0.1)
plt.fill_between(x,z2,facecolor='steelblue', alpha=0.5)
plt.plot(x,z*0.048,c='firebrick',linewidth=2,label='Likelihood')
plt.plot(x,z2,c='grey',linewidth=2,linestyle='--',label='Posterior')

plt.scatter(mux,cumy,c='firebrick')
plt.axvline(mux,c='grey',linewidth=0.5)
plt.legend()
plt.xlim(mu-3*sigma,mu+4*sigma)
plt.ylim(0,0.0482)
plt.xlabel('Skill $s_{i}$')
plt.ylabel('Density')
plt.xticks(ticks=[0,mu],labels=[0,r'$\mu_i$'])
plt.yticks(ticks=[0],labels=[0])
plt.savefig(f'./{name}.pdf')

#%%
plt.figure(1)
x0 = x[250]
xdiff = mu-muL
plt.plot(x,diff,c='steelblue',linewidth=2,linestyle=':')


plt.text(1,0.002,'Probability of winner')
plt.fill_between(x[:251], diff[:251], facecolor='steelblue', alpha=0.2)

plt.fill_between(x[250:], diff[250:], facecolor='steelblue', alpha=0.5)


plt.axvline(x0,c='grey',linewidth=1)
plt.axvline(xdiff,c='firebrick',linewidth=1)

plt.xlim(-mu,mu+5)
plt.ylim(0,0.0482)
plt.xlabel('Skill $d_{ij}$')
plt.ylabel('Density')
plt.xticks(ticks=[0,xdiff],labels=[0,r'$d_{ij}$'])
#plt.yticks(ticks=[0],labels=[0])
plt.savefig(f'./{name}_diff.pdf')
