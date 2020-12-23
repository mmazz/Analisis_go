import sys
sys.path.append('./')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
name = os.path.basename(__file__).split(".py")[0]

# para mu mostrar diferentes curvas de diferentes mus, pero mostrar que
# la diferencia relativa  no cambia. Tambien que la evidencia es igual.
################################################
############### Mu  ONLINE  #####################
################################################
csv_mu = "./Datos/SM_mu_lc.csv"
#csv_mu_20 = "./Datos/SM_mu_lc_20.csv"

df = pd.read_csv(csv_mu)

#df = df[["ts_0","ttt_0","ts_12_5","ttt_12_5","ts_25","ttt_25"]][:175]
plt.figure(0)

plt.plot("ts_0", data=df,c='firebrick',marker='*',markersize=4,linewidth=2, label="TrueSkill $\mu_0$=0")
plt.plot("ttt_0", data=df,c='steelblue',linewidth=2, label="TTT $\mu_0$=0")
plt.xlabel("Number of games")
plt.ylabel("$\mu$ (Mean)")
#plt.xlim(0.0, 0.4)
#plt.ylim(-860, -820)
plt.legend(fontsize=15)
#plt.show()
plt.savefig(f'./{name}_mu_jugador0.pdf')
plt.figure(1)
plt.plot("ts_12_5", data=df,c='firebrick', marker='*',markersize=4,linewidth=2, label="TrueSkill $\mu_0$=12.5")
plt.plot("ttt_12_5", data=df,c='steelblue',linewidth=2, label="TTT $\mu_0$=12.5")
plt.xlabel("Number of games")
plt.ylabel("$\mu$ (Mean)")
#plt.xlim(0.0, 0.4)
#plt.ylim(-860, -820)

plt.legend(fontsize=15)
#plt.show()
plt.savefig(f'./{name}_mu_jugador12_5.pdf')
plt.figure(2)
plt.plot("ts_25", data=df,c='firebrick', marker='*',markersize=4,linewidth=2, label="TrueSkill $\mu_0$=25")
plt.plot("ttt_25", data=df,c='steelblue',linewidth=2, label="TTT $\mu_0$=25")
# evidencia mu -3037.66
#df_20.plot(ax=ax)
plt.xlabel("Number of games")
plt.ylabel("$\mu$ (Mean)")
#plt.xlim(0.0, 0.4)
#plt.ylim(-860, -820)
plt.legend(fontsize=15)
#plt.show()
plt.savefig(f'./{name}_mu_jugador25.pdf')

#csv_mu_ev = "./Datos/SM_evidencia_mu.csv"
#df = pd.read_csv(csv_mu_ev)


csv_sigma_ev = "./Datos/SM_evidencia_sigma.csv"
df_ev = pd.read_csv(csv_sigma_ev)
mints = df_ev.loc[df_ev['Evidencia_ts'].idxmin(), 'Sigma']
minttt = df_ev.loc[df_ev['Evidencia_ttt'].idxmin(), 'Sigma']

plt.figure(3)

plt.plot("Sigma", "Evidencia_ts", data=df_ev,c='firebrick', linestyle=':',linewidth=3, label="TrueSkill", zorder=5)
plt.plot("Sigma", "Evidencia_ttt", data=df_ev,c='steelblue',linewidth=3, label="TTT", zorder=5)
plt.scatter(mints, df_ev['Evidencia_ts'].min(), data=df_ev,c='orange',linewidth=2, zorder=15)
plt.scatter(minttt, df_ev['Evidencia_ttt'].min(), data=df_ev,c='cyan',linewidth=2, zorder=15)
plt.axvline(1.2,c='black',linestyle='--',linewidth=1, zorder=25)
plt.text(1.25,-540,r'$\sigma$=1.2')

plt.xlabel("$\sigma_0$ (Sigma)")
plt.ylabel("Evidence")
plt.xlim(0.1, 4.0)
plt.ylim(0.43, 0.57)
plt.legend()
plt.savefig(f'./{name}_sigma_ev.pdf')

################################################
###############SIGMA  ONLINE  #####################
################################################

csv_sigma = "./Datos/SM_sigma_lc_online.csv"
df = pd.read_csv(csv_sigma)

plt.figure(4)
#df_mu.plot()
plt.plot("ts_0001", data=df,c='red', linestyle='--', linewidth=2, label="TrueSkill $\sigma_0$=0.0001")
plt.plot("ttt_0001", data=df,c='b',linewidth=2, label="TTT $\sigma_0$=0.0001")
plt.plot("ts_3", data=df,c='green',linewidth=2, linestyle='--', label="TrueSkill $\sigma_0$=3")
plt.plot("ttt_3", data=df,c='steelblue',linewidth=2, label="TTT $\sigma_0$=3")
plt.plot("ts_10", data=df,c='firebrick',linewidth=2, linestyle='--', label="TrueSkill $\sigma_0$=10")
plt.plot("ttt_10", data=df,c='purple',linewidth=2, label="TTT $\sigma_0$=10")

plt.xlabel("Number of games")
plt.ylabel("$\sigma$ (Sigma)")
#plt.xlim(0.0, 70)
#plt.ylim(24.5, 28)
plt.legend()
plt.savefig(f'./{name}_sigma_sin_cambios.pdf')
#plt.savefig('./Sigma_mu_jugador.pdf')

csv_mu = "./Datos/SM_sigma_lc_mu_online.csv"
df_mu = pd.read_csv(csv_mu)
plt.figure(5)
#df_mu.plot()
plt.plot("ts_0001", data=df_mu,c='red',linewidth=2, linestyle='--', label="TrueSkill $\sigma_0$=0.0001")
plt.plot("ttt_0001", data=df_mu,c='b',linewidth=2, label="TTT $\sigma_0$=0.0001")
plt.plot("ts_3", data=df_mu,c='green',linewidth=2, linestyle='--', label="TrueSkill $\sigma_0$=3")
plt.plot("ttt_3", data=df_mu,c='steelblue',linewidth=2, label="TTT $\sigma_0$=3")
plt.plot("ts_10", data=df_mu,c='firebrick',linewidth=2, linestyle='--', label="TrueSkill $\sigma_0$=10")
plt.plot("ttt_10", data=df_mu,c='purple',linewidth=2, label="TTT $\sigma_0$=10")

plt.xlabel("Number of games")
plt.ylabel("$\mu$ (Mean)")
#plt.xlim(0.0, 70)
#plt.ylim(24.5, 28)
plt.legend()
#plt.show()
plt.savefig(f'./{name}_sigma_lc.pdf')

#df = pd.read_csv("./Datos/SM_evidencia_sigma.csv")




################################################
############### BETA ONLINE  #####################
################################################
csv_mu = "./Datos/SM_beta_lc_mu_online.csv"
df_mu = pd.read_csv(csv_mu)
plt.figure(6)
#df_mu.plot()
#plt.plot("ts_01", data=df_mu,c='red', marker='*',markersize=4, linewidth=1, label="TrueSkill \u03B2$_0$=0.01")
#plt.plot("ttt_01", data=df_mu,c='b',linewidth=2, label="TTT \u03B2$_0$=0.01")
plt.plot("ts_1", data=df_mu,c='red',linewidth=2, linestyle='--', label="TrueSkill \u03B2=1")
plt.plot("ttt_1", data=df_mu,c='green',linewidth=2, label="TTT \u03B2=1")
plt.plot("ts_5", data=df_mu,c='cyan',linewidth=2, linestyle='--', label="TrueSkill \u03B2=5")
plt.plot("ttt_5", data=df_mu,c='purple',linewidth=2, label="TTT \u03B2=5")
plt.plot("ts_10", data=df_mu,c='firebrick',linewidth=2, linestyle='--', label="TrueSkill \u03B2=10")
plt.plot("ttt_10", data=df_mu,c='steelblue',linewidth=2, label="TTT \u03B2$=10")
#plt.plot("ts_100", data=df_mu,c='orange', marker='*',linewidth=2, label="TS \u03B2$_0$=100")
#plt.plot("ttt_100", data=df_mu,c='purple',linewidth=2, label="TTT \u03B2$_0$=100")

plt.xlabel("Number of games")
plt.ylabel("$\mu$ (Mean)")
#plt.xlim(0.0, 70)
#plt.ylim(24.5, 28)
plt.legend()
#plt.show()
plt.savefig(f'./{name}_beta_lc.pdf')

#csv_mu = "./Datos/SM_evidencia_proba_beta.csv"
#df_mu = pd.read_csv(csv_mu)
#df_mu=df_mu[["Beta","Sigma", "Evidencia_ts", "Evidencia_ttt","Mu 1", "Mu 2", "proba_1vs2"]]
#print(df_mu)
