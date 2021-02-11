import matplotlib.pyplot as plt
import numpy as np
import random
import math
import os
name = os.path.basename(__file__).split(".py")[0]

random.seed(42)

m_real = 50
sigma_prior = 100
m_prior = 0
leng = 10000
num_data = 5
m = np.linspace(m_prior-3*sigma_prior, m_prior + 3*sigma_prior, leng)
Nm = np.zeros(leng)
likelihood_x = np.zeros((num_data, leng))
x = np.zeros(num_data) # las observaciones
Prodlikelihood = 1


def gauss(x, mu, sigma):
    y = 1/(sigma*(math.sqrt(2*math.pi)))*math.exp(-0.5*((x-mu)/sigma)**2)
    return y


for i in range(leng): # el prior
    Nm[i] = gauss(m[i], m_prior, sigma_prior)

for i in range(num_data):
    x[i] = np.random.normal(loc=m_real, scale=1)


for i in range(num_data):
    for j in range(leng):
        #likelihood_x[i][j] = gauss(pm[j], x[i], 1) # estos estan normalizados
        likelihood_x[i][j] = 1/2*gauss(m[j], x[i], 1) + 1/2*gauss(x[i], 0, 1)

for i in range(num_data):
    Prodlikelihood = Prodlikelihood*likelihood_x[i][:] # estos parecen no estar normalizados


posterior = Prodlikelihood*Nm


z = 0
l = 0
n = 0
delta = m[1]-m[0]
print(delta)
for i in range(leng):
    l += Prodlikelihood[i]*delta
    z += posterior[i]*delta
    n += likelihood_x[1][i]*delta
print(l,z,n)
for i in range(leng):
    posterior[i] = posterior[i]/z
    Prodlikelihood[i] = Prodlikelihood[i]/l

plt.plot(m, posterior, label="Posterior")
plt.plot(m, Nm, label='Prior')
plt.plot(m, Prodlikelihood, label="Likelhood")
plt.legend(title=f"Real mean = {m_real}")
plt.show()
