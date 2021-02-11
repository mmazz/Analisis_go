import numpy as np
import matplotlib.pyplot as plt
import src as ttt
import os
name = os.path.basename(__file__).split(".py")[0]
N = ttt.Gaussian(mu=25,sigma=25/3)



mu= 25
sigma = 25/3
LENG = 1000
proporcion = 5/7
x = np.linspace(mu-3*sigma,mu+3*sigma,LENG)
y = np.linspace(mu-3*sigma,mu+3*sigma,LENG)
z = np.linspace(mu-3*sigma,mu+3*sigma,LENG)

print(N.trunc(30,True))
def gaus(x,mu,sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


print(x[int(5/7*LENG)])
index = int(proporcion*LENG)

muTrunc, sigmaTrunc = ttt.Gaussian(mu,sigma).trunc(x[index],True)

for i in range(len(x)):
    y[i] = gaus(x[i], muTrunc, sigmaTrunc)
    if i <= int(3/5*LENG):
        z[i] = gaus(x[i], mu, sigma)
    else:
        z[i] = 0

plt.plot(x, z, c='steelblue', linewidth=2, label="Truncada")
plt.plot(x, y, c='firebrick', linewidth=2, linestyle='--', label="Aproximacion")
plt.axvline(mu, c='black', linewidth=1.5, linestyle='--')
plt.xticks(ticks=[mu-3*sigma,mu-2*sigma,mu-sigma,mu,mu+sigma,mu+2*sigma,mu+3*sigma],labels=[r'$\mu-3\sigma$',r'$\mu-2\sigma$',r'$\mu-\sigma$',r'$\mu$',r'$\mu+\sigma$',r'$\mu+2\sigma$',r'$\mu+3\sigma$'],fontsize=14)
plt.yticks([],[])
plt.legend(fontsize=14)
plt.ylabel('Densidad',fontsize=14)
plt.show()
#plt.savefig(f'../{name}.pdf')
