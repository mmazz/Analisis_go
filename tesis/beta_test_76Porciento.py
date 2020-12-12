import numpy as np


def gaus(x, mu, sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


mu = 25
beta = 1.0/(0.21844648724*1.011657753913105*1.0162)
sigma = 3*beta
leng = 100000

x = np.linspace(beta-6*sigma, beta+6*sigma, leng)
y = np.zeros(leng)
z = np.zeros(leng)
delta = x[1]-x[0]

# En caso de tener handicap, tendria otro beta mas de incertidumbre? no beta_h=0
diff_skill = beta
#diff_skill = 0.69+0.5
for i in range(len(x)):
    y[i] = gaus(x[i], diff_skill, np.sqrt(2*beta**2))

for i in range(len(x)):
    if i == 0:
        z[i] = y[i]*delta
    else:
        z[i] = z[i-1] + y[i]*delta

ind_cero = np.abs(x).argmin()
print('Prob de ganar: ', round(1-z[ind_cero],3), '%')
