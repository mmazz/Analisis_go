import sys
sys.path.append('./')
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


########################################
csv_ev = "./SV_ev2.csv"
df = pd.read_csv(csv_ev)

minttt = df.loc[df['evidencias_ttt'].idxmin(), 'gammas']
mints = df.loc[df['evidencias_ts'].idxmin(), 'gammas']
gamma = 0.02
print(mints)
print(minttt)
plt.figure(1)
plt.plot("gammas", "evidencias_ts", data=df,c='firebrick',linewidth=2, label="TrueSkill",zorder=10)
plt.plot("gammas", "evidencias_ttt", data=df,c='steelblue',linewidth=2, label="TTT",zorder=10)
plt.scatter(mints, df['evidencias_ts'].min(), data=df,c='orange',linewidth=2,zorder=20)
plt.scatter(minttt, df['evidencias_ttt'].min(), data=df,c='cyan',linewidth=2,zorder=20)
plt.axvline(gamma,c='black',linestyle='--',linewidth=1)
plt.text(0.02,-835,r'$\gamma$ = 0.015')

plt.xlabel("Gamma $\gamma$")
plt.ylabel("Evidence")
plt.xlim(0.0, 0.1)
plt.ylim(0.82, 0.8325)
plt.legend()
#plt.show()
plt.savefig(f'../img/synthetic_validation_gamma_evidencia2.pdf')


csv = "./SV2.csv"
df = pd.read_csv(csv)
plt.figure(2)
plt.plot("mean_agent", data=df,c='firebrick',linewidth=2, label="Truth",zorder=20)
plt.plot("lc_0005", data=df,c='purple',linewidth=1,linestyle='--', label="$\gamma$ = 0.005",zorder=10)
plt.plot("lc_002", data=df,c='steelblue',linewidth=2, label="$\gamma$ = 0.02",zorder=20)
plt.plot("lc_01", data=df,c='olive',linewidth=1,linestyle='--', label="$\gamma$ = 0.1",zorder=10)
plt.xlabel("Number of games")
plt.ylabel("Mean")
plt.legend()
plt.savefig(f'../img/synthetic_validation_lc_evidencia2.pdf')

#plt.show()
