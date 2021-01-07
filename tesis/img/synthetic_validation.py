import sys
sys.path.append('./')
import os
name = os.path.basename(__file__).split(".py")[0]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csv_abc = "./Datos/SV_abc.csv"
df = pd.read_csv(csv_abc)
#print(df.mu_a_ttt)
#plt.figure(3)
#plt.plot("mu_a_ts", data=df,c='firebrick',linewidth=2,linestyle='--', label="Real")
#plt.show()

##############################33
csv_abc3 = "./Datos/SV_same_strength.csv"
df = pd.read_csv(csv_abc3)
####################################
# Se realiza en un mismo bache, de esta forma el gamma es cero. Es lo MEJOR
# que puede predecir el modelo.

csv_two_groups = "./Datos/SV_same_strength_two_groups_1.csv"
df = pd.read_csv(csv_two_groups)
csv_two_groups_2 = "./Datos/SV_same_strength_two_groups_2.csv"
df_2 = pd.read_csv(csv_two_groups_2)
csv_two_groups_3 = "./Datos/SV_same_strength_two_groups_3.csv"
df_3 = pd.read_csv(csv_two_groups_3)
plt.figure(0)
'''
print(df["mle"].values[-1])
mle1 = df["mle"].values[-1]
mle2 = df_2["mle"].values[-1]
mle3 = df_3["mle"].values[-1]
aiaj1 = df["aiaj"].values[-1]
aiaj2 = df_2["aiaj"].values[-1]
aiaj3 = df_3["aiaj"].values[-1]
df["mle"] = df["mle"]/mle1
df_2["mle"] = df_2["mle"]/mle2
df_3["mle"] = df_3["mle"]/mle3
df["aiaj"] = df["aiaj"]/aiaj3
df_2["aiaj"] = df_2["aiaj"]/aiaj2
df_3["aiaj"] = df_3["aiaj"]/aiaj3
'''

plt.figure(0)
plt.plot("mle", "mle", data=df,c='firebrick',linewidth=2,linestyle='--', label="Truth")
plt.plot("mle", "aiaj", data=df_3,c='green',marker='*',linewidth=2, label="TTT information$x$4")
plt.plot("mle", "aiaj", data=df_2,c='orange',marker='*',linewidth=2, label="TTT information$x$2")
plt.plot("mle", "aiaj", data=df,c='steelblue',marker='*',linewidth=2, label="TTT information$x$1")
plt.xlabel("Fraction of wins")
plt.ylabel("Probability of winning")
#plt.xlim(0.0, 0.4)
#plt.ylim(-860, -820)
plt.legend()
#plt.show()
plt.savefig(f'./{name}_model_limit.pdf')
########################################
csv_ev = "./Datos/SV_best_gamma_evidences.csv"
df = pd.read_csv(csv_ev)

minttt = df.loc[df['evidencias_ttt'].idxmin(), 'gammas']
mints = df.loc[df['evidencias_ts'].idxmin(), 'gammas']
gamma = 0.015
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
plt.savefig(f'./{name}_gamma_evidencia.pdf')

csv = "./Datos/SV_best_gamma_lc.csv"
df = pd.read_csv(csv)
plt.figure(2)
plt.plot("mean_agent", data=df,c='firebrick',linewidth=2, label="Truth",zorder=20)
plt.plot("lc_0005", data=df,c='purple',linewidth=1,linestyle='--', label="$\gamma$ = 0.005",zorder=10)
plt.plot("lc_0015", data=df,c='steelblue',linewidth=2, label="$\gamma$ = 0.015",zorder=20)
plt.plot("lc_01", data=df,c='olive',linewidth=1,linestyle='--', label="$\gamma$ = 0.1",zorder=10)
plt.xlabel("Number of games")
plt.ylabel("Mean")
plt.legend()
#plt.show()
plt.savefig(f'./{name}_lc_evidencia.pdf')
