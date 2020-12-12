import os
name = os.path.basename(__file__).split(".py")[0]
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
leng = -500000

df = pd.read_csv("./rela_beta_sigma_zoom.csv")
df2 = pd.read_csv("./rela_beta_sigma_zoom_noH.csv")
#df3 = pd.read_csv("./Datos/rela_beta_sigma_zoom_H1.csv")
df["tres_beta_ts"] = df["tres_beta_ts"]/leng
df["tres_beta_ttt"] = df["tres_beta_ttt"]/leng
df2["tres_beta_ts"] = df2["tres_beta_ts"]/leng
df2["tres_beta_ttt"] = df2["tres_beta_ttt"]/leng
#df3["tres_beta_ttt"] = df3["tres_beta_ttt"]/leng

maxttt = df.loc[df['tres_beta_ttt'].idxmin(), 'gammas']
maxttt2 = df2.loc[df2['tres_beta_ttt'].idxmin(), 'gammas']
#maxttt3 = df3.loc[df['tres_beta_ttt'].idxmin(), 'gammas']
maxts = df.loc[df['tres_beta_ts'].idxmin(), 'gammas']
maxts2 = df2.loc[df2['tres_beta_ts'].idxmin(), 'gammas']

print("Optimal gamma for TTT with all handicaps: ", maxttt)
fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel("Gamma $\gamma$")
ax1.set_ylabel('Evidence TTT', color=color)
ax1.plot("gammas", "tres_beta_ttt", data=df, c='steelblue',linewidth=2, label="TTT with handicap")
ax1.plot("gammas", "tres_beta_ttt", data=df2, c='steelblue',  linewidth=2,linestyle='dashed', label="TTT")
#ax1.plot("gammas", "tres_beta_ttt", data=df3,c='forestgreen',linewidth=2, label="TTT $\sigma_0$=3\u03B2$_0$ no H1 ")

ax1.scatter(maxttt, df['tres_beta_ttt'].min(), data=df, c='cyan', linewidth=2)#, label="Max evidence TTT")
ax1.scatter(maxttt2, df2['tres_beta_ttt'].min(), data=df2, c='cyan', linewidth=2, label="Min evidence TTT")#, label="Max evidence TTT")
#ax1.scatter(maxttt3, df3['tres_beta_ttt'].min(), data=df3,c='limegreen',linewidth=2)#, label="Max evidence TTT")
ax1.set_xlim(0, 0.03)

ax1.tick_params(axis='y', labelcolor=color)
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('Evidence TS', color=color)  # we already handled the x-label with ax1
ax2.plot("gammas", "tres_beta_ts", data=df, c='firebrick', linewidth=2, label="TrueSkill  with handicap")
ax2.plot("gammas", "tres_beta_ts", data=df2, c='firebrick', linewidth=2,linestyle='dashed',  label="TrueSkill")

ax2.scatter(maxts, df['tres_beta_ts'].min(), data=df, c='red', linewidth=2, label="Min evidence TrueSkill")
ax2.scatter(maxts2, df2['tres_beta_ts'].min(), data=df2, c='red', linewidth=2)

ax2.tick_params(axis='y', labelcolor=color)
#fig.legend(loc="center right")

fig.legend( bbox_to_anchor=(0.35, 0.06, 0.5, 0.5))
fig.tight_layout()  # otherwise the right y-label is slightly clipped
#plt.ylabel("Evidence")

plt.savefig(f'./{name}.pdf')
