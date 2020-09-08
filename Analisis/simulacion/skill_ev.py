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

Jugadores_k = list(Jugadores_TS.keys())
for i in range(len(Jugadores_TS)):
    Jugador_key = Jugadores_k[i]
    x_TS = np.linspace(0, len(Jugadores_TS[Jugador_key]),len(Jugadores_TS[Jugador_key]))
    y_TS = Jugadores_TS[Jugador_key]
    z_TS = Jugadores_TS_std[Jugador_key]
    x_TTT = np.linspace(0, len(Jugadores_TTT[Jugador_key]),len(Jugadores_TTT[Jugador_key]))
    y_TTT = Jugadores_TTT[Jugador_key]
    z_TTT = Jugadores_TTT_std[Jugador_key]
    x_Real = np.linspace(0, len(Jugadores_real[Jugador_key]),len(Jugadores_real[Jugador_key]))
    y_Real = Jugadores_real[Jugador_key]
    plt.figure(0)
    plt.plot(x_Real, y_Real, label='Real')
    plt.plot(x_TS, y_TS, label='TS')
    plt.plot(x_TTT, y_TTT, label='TTT')
    plt.legend()
    #plt.show()
    plt.figure(1)
    plt.plot(x_TS, z_TS, label='TS')
    plt.plot(x_TTT, z_TTT, label='TTT')
    plt.legend()
    #plt.show()
    print(Jugador_key, 'real:',  y_Real[-1], ' TrueSkill:(mu= ',y_TS[-1],'sigma=', z_TS[-1], ')')
    print('TTT:', y_TTT[-1], z_TTT[-1])
