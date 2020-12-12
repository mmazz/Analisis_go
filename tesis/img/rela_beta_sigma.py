import os
name = os.path.basename(__file__).split(".py")[0]
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
leng = -500000

df = pd.read_csv("./rela_beta_sigma.csv")
df["tres_beta"] = df["tres_beta"]/leng
df["seis_beta"] = df["seis_beta"]/leng
df["nueve_beta"] = df["nueve_beta"]/leng
max3 = df.loc[df['tres_beta'].idxmin(), 'gammas']
max6 = df.loc[df['seis_beta'].idxmin(), 'gammas']
max10 = df.loc[df['nueve_beta'].idxmin(), 'gammas']
df["tres_beta"] = df["tres_beta"]/df['tres_beta'].max()
df["seis_beta"] = df["seis_beta"]/df['seis_beta'].max()
df["nueve_beta"] = df["nueve_beta"]/df['nueve_beta'].max()

plt.figure(1)
plt.plot("gammas", "nueve_beta", data=df, c='firebrick', linewidth=2, label="$\sigma_0$=9\u03B2", zorder=5)
plt.plot("gammas", "seis_beta", data=df, c='green', linewidth=2, label="$\sigma_0$=6\u03B2", zorder=5)
plt.plot("gammas", "tres_beta", data=df, c='steelblue', linewidth=2, label="$\sigma_0$=3\u03B2", zorder=5)

plt.scatter(max3, df['tres_beta'].min(), data=df, c='orange', linewidth=2, label="Min evidence", zorder=15)
plt.scatter(max6, df['seis_beta'].min(), data=df, c='orange', linewidth=2, zorder=15)
plt.scatter(max10, df['nueve_beta'].min(), data=df, c='orange', linewidth=2, zorder=15)

plt.xlabel("Gamma $\gamma$")
plt.ylabel("Evidence")
plt.yticks([])
#plt.xlim(0.0, 140)
#plt.ylim(-0.1, 1)
plt.legend()
#plt.yscale('log')
#plt.xscale('log')
#plt.show()
plt.savefig(f'./{name}.pdf')
print("Max evidence gamma beta=3sigma:", max3)
