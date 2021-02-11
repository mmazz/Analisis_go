import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.stats import norm
import os
name = os.path.basename(__file__).split(".py")[0]

random.seed(42)

m_real = 50
sigma_prior = 10
m_prior = 40
leng = 10000
num_data = 1
m = np.linspace(m_prior-3*sigma_prior, m_prior + 3*sigma_prior, leng)
Nm = np.zeros(leng)
likelihood_x = np.zeros((num_data, leng))
x = np.zeros(num_data) # las observaciones
Prodlikelihood = 1


Nm = norm.pdf(m, loc=m_prior, scale=sigma_prior)
for i in range(num_data):
    x[i] = norm.rvs(loc=m_real, scale=1, size=1)
    likelihood_x[i][:] = 1/2*norm.pdf(m,  loc=x[i], scale=1) + 1/2*norm.pdf(x[i], loc=0, scale=1)
    Prodlikelihood = Prodlikelihood*likelihood_x[i][:]

posterior = Prodlikelihood*Nm

z = 0
delta = m[1]-m[0]
print(delta)
for i in range(leng):
    z += posterior[i]*delta


plt.plot(m, posterior/z, label="Posterior")
plt.plot(m, Nm, label='Prior')
plt.plot(m, Prodlikelihood, label="Likelhood")
plt.legend(title=f"Real mean = {m_real}")
plt.show()
