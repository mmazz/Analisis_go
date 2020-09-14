import sys
sys.path.append('./')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csv_TS = './Trueskill_datos_sin_handicap.csv'
csv_TTT = './TTT_datos_sin_handicap.csv'
csv_Real = './simulacion.csv'
df_TS = pd.read_csv(csv_TS)
df_TTT = pd.read_csv(csv_TTT)


#Jugadores = {'pepe': [25, 0], 'juan': [30, 0], 'ruben': [35, 0], 'lol': [40, 0]}
Jugadores_TS = {}
Jugadores_TTT = {}
Jugadores_real = {}
Jugadores_TS_std = {}
Jugadores_TTT_std = {}

for i in df_TTT.index:
    p1_key = str(df_TTT.loc[i].white)
    p2_key = str(df_TTT.loc[i].black)
    Jugadores_TS[p1_key]= []
    Jugadores_TS[p2_key]= []
    Jugadores_TTT[p1_key]= []
    Jugadores_TTT[p2_key]= []
    Jugadores_real[p1_key]= []
    Jugadores_real[p2_key]= []
    Jugadores_TS_std[p1_key]= []
    Jugadores_TS_std[p2_key]= []
    Jugadores_TTT_std[p1_key]= []
    Jugadores_TTT_std[p2_key]= []

for i in df_TTT.index:
    p1_key = str(df_TTT.loc[i].white)
    p2_key = str(df_TTT.loc[i].black)
    Jugadores_TS[p1_key].append(df_TS.loc[i].w_mean)
    Jugadores_TS[p2_key].append(df_TS.loc[i].b_mean)
    Jugadores_TTT[p1_key].append(df_TTT.loc[i].w_mean)
    Jugadores_TTT[p2_key].append(df_TTT.loc[i].b_mean)
    Jugadores_real[p1_key].append(df_TTT.loc[i].white_skill)
    Jugadores_real[p2_key].append(df_TTT.loc[i].black_skill)
    Jugadores_TS_std[p1_key].append(df_TS.loc[i].w_std)
    Jugadores_TS_std[p2_key].append(df_TS.loc[i].b_std)
    Jugadores_TTT_std[p1_key].append(df_TTT.loc[i].w_std)
    Jugadores_TTT_std[p2_key].append(df_TTT.loc[i].b_std)

# acomodo los jugadores en menor a mayor de habilidad real. (todos tienen fija)
Jugadores_k = list(Jugadores_TS.keys())
sort_orders = sorted(Jugadores_real.items(), key=lambda x: x[1], reverse=False)
index = 0
for i in sort_orders:
    Jugadores_k[index] = i[0]
    index += 1

print(Jugadores_k)
x_TS = {}
y_TS = {}
z_TS = {}
x_TTT = {}
y_TTT = {}
z_TTT = {}
x_Real = {}
y_Real = {}
mu_jugadores_TTT = {}
mu_jugadores_reales = {}

for i in range(len(Jugadores_k)):
    Jugador_key = Jugadores_k[i]
    x_TS[Jugador_key] = np.linspace(0, len(Jugadores_TS[Jugador_key]),len(Jugadores_TS[Jugador_key]))
    y_TS[Jugador_key] = Jugadores_TS[Jugador_key]
    z_TS[Jugador_key] = Jugadores_TS_std[Jugador_key]

    x_TTT[Jugador_key] = np.linspace(0, len(Jugadores_TTT[Jugador_key]),len(Jugadores_TTT[Jugador_key]))
    y_TTT[Jugador_key] = Jugadores_TTT[Jugador_key]
    z_TTT[Jugador_key] = Jugadores_TTT_std[Jugador_key]

    x_Real[Jugador_key] = np.linspace(0, len(Jugadores_real[Jugador_key]),len(Jugadores_real[Jugador_key]))
    y_Real[Jugador_key] = Jugadores_real[Jugador_key]
    mu_jugadores_TTT[Jugador_key] = y_TTT[Jugador_key][-1]
    mu_jugadores_reales[Jugador_key] = y_Real[Jugador_key][-1]
    print(mu_jugadores_TTT)
    plt.figure(0)
    plt.title('Mu')
    plt.plot(x_Real[Jugador_key], y_Real[Jugador_key], label='Real')
    plt.plot(x_TS[Jugador_key], y_TS[Jugador_key], label='TS')
    plt.plot(x_TTT[Jugador_key], y_TTT[Jugador_key], label='TTT')
    plt.legend()
    plt.show()
    plt.figure(1)
    plt.title('Sigma')
    plt.plot(x_TS[Jugador_key], z_TS[Jugador_key], label='TS')
    plt.plot(x_TTT[Jugador_key], z_TTT[Jugador_key], label='TTT')
    plt.legend()
    plt.show()
    #print(Jugador_key, 'real:',  y_Real[Jugador_key][-1], ' TrueSkill:(mu= ',y_TS[Jugador_key][-1],'sigma=', z_TS[-1], ')')
    #print('TTT:', y_TTT[Jugador_key][-1], z_TTT[Jugador_key][-1])

    #print(Jugador_key, 'real:',  y_Real[Jugador_key][-1], ' TTT:(mu= ',y_TTT[Jugador_key][-1],'sigma=', z_TS[Jugador_key][-1], ')')


diff_TTT = [None]*(len(sort_orders)-1)
diff_Real = [None]*(len(sort_orders)-1)

for i in range(len(Jugadores_k)-1):
    print(sort_orders[i+1][0], '-', sort_orders[i][0])
    J1_Real = mu_jugadores_reales[sort_orders[i+1][0]]
    J2_Real = mu_jugadores_reales[sort_orders[i][0]]
    diff_Real[i] = (J1_Real - J2_Real)/mu_jugadores_reales[sort_orders[0][0]]
    J1_TTT = mu_jugadores_TTT[sort_orders[i+1][0]]
    J2_TTT = mu_jugadores_TTT[sort_orders[i][0]]
    diff_TTT[i] = (J1_TTT - J2_TTT)/mu_jugadores_TTT[sort_orders[0][0]]
print(diff_Real)
print(diff_TTT)
