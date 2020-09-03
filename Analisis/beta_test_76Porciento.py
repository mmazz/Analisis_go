import numpy as np


def gaus(x, mu, sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


mu = 25
sigma = 25/3
beta = 25/6
leng = 100000

x = np.linspace(beta-6*sigma, beta+6*sigma, leng)
y = np.zeros(leng)
z = np.zeros(leng)
delta = x[1]-x[0]

for i in range(len(x)):
    y[i] = gaus(x[i], beta, np.sqrt(2*beta**2))

for i in range(len(x)):
    if i == 0:
        z[i] = y[i]*delta
    else:
        z[i] = z[i-1] + y[i]*delta

ind_cero = np.abs(x).argmin()
print('Prob de ganar: ', 1-z[ind_cero], '%')
