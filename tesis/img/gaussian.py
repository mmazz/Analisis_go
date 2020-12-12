#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 11:58:53 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import matplotlib.pyplot as plt

mu= 25
sigma = 25/3
x = np.linspace(-mu,3*mu,1000)
y = np.linspace(-mu,3*mu,1000)



def gaus(x,mu,sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y

for i in range(len(x)):
    y[i] = gaus(x[i],mu,sigma)

 #%%
#Grillado
plt.figure(0)
plt.plot(x,y,c='steelblue',linewidth=2)
plt.axvline(x=mu-4*sigma,c='grey',linewidth=0.5)
plt.fill_between(x[161:250],y[161:250],facecolor='steelblue', alpha=0.1)
plt.axvline(x=mu-3*sigma,c='grey',linewidth=0.5)
plt.fill_between(x[250:334],y[250:334],facecolor='steelblue', alpha=0.2)
plt.axvline(x=mu-2*sigma,c='grey',linewidth=0.5)
plt.fill_between(x[333:417],y[333:417],facecolor='steelblue', alpha=0.3)
plt.axvline(x=mu-sigma,c='grey',linewidth=0.5)
plt.fill_between(x[416:584],y[416:584],facecolor='steelblue', alpha=0.5)
plt.axvline(x=mu,c='firebrick',linewidth=2)
plt.fill_between(x[583:667],y[583:667],facecolor='steelblue', alpha=0.3)
plt.axvline(x=mu+sigma,c='grey',linewidth=0.5)
plt.fill_between(x[666:751],y[666:751],facecolor='steelblue', alpha=0.2)
plt.axvline(x=mu+2*sigma,c='grey',linewidth=0.5)
plt.fill_between(x[750:],y[750:],facecolor='steelblue', alpha=0.1)
plt.axvline(x=mu+3*sigma,c='grey',linewidth=0.5)
plt.axvline(x=mu+4*sigma,c='grey',linewidth=0.5)

plt.hlines(0.028,mu,mu+sigma,colors='g',linewidth=2,label=' asd')

#%%
#text
plt.text(mu+2.5*sigma/6,0.029,r'$\sigma$')
plt.text(mu-5*sigma/6,0.02,'34,1%')
plt.text(mu-11*sigma/6,0.005,'13,6%')
plt.text(mu-16*sigma/6,0.0005,'2,1%')
plt.text(mu+1*sigma/6,0.02,'34,1%')
plt.text(mu+7*sigma/6,0.005,'13,6%')
plt.text(mu+13*sigma/6,0.0005,'2,1%')


plt.xlim(-5,55)
plt.ylim(0,0.05)
plt.ylabel('Density')
plt.xticks(ticks=[mu-3*sigma,mu-2*sigma,mu-sigma,mu,mu+sigma,mu+2*sigma,mu+3*sigma],labels=[r'$\mu-3\sigma$',r'$\mu-2\sigma$',r'$\mu-\sigma$',r'$\mu$',r'$\mu+\sigma$',r'$\mu+2\sigma$',r'$\mu+3\sigma$'])
plt.savefig(f'./{name}.pdf')

#%%
plt.figure(1)
z = np.zeros(1000)
delta=x[1]-x[0]

for i in range(len(x)):
    y[i] = gaus(x[i],0,1)
    if i == 0:
        z[i] =y[i]*delta
    else:
        z[i]=z[i-1] + y[i]*delta
plt.plot(x,y,c='steelblue',linewidth=2)
x0 = x[:241]
plt.text(x[240]+0.1,z[241]-0.04,round(z[240],3))
plt.fill_between(x0,y[:241],facecolor='steelblue', alpha=0.5)
plt.plot(x,z,c='firebrick',linewidth=2)
plt.scatter(x[240],z[240],c='firebrick')
plt.axvline(x=x[240],c='grey',linewidth=0.5)
plt.xlim(-3,3)
plt.ylim(0,1.1)
plt.savefig(f'./{name}_cumulative.pdf')
