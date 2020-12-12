#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
"""
import pandas as pd
import os
name = os.path.basename(__file__).split(".py")[0]


'''
Vemos de estimar partidas que usaron handicap y sin.
De esa forma si hay cambio entre estas dos estimaciones, da fuerza a
que se asigno mal la cantidad de handicap.
'''
#df_ts_h = pd.read_csv('../img/Datos/TS_datos_con_handicap_zoom.csv')
#df_TTT_h = pd.read_csv('../img/Datos/TTT_datos_con_handicap_zoom.csv')
df_TTT_h = pd.read_csv('./TTT_H_uno.csv')
#agarro estos ya que quiero que se parezca mas a algo online.
# si miro ttt, en la aprtida que estoy agarrando quizas fue una de las primeras
# y caudno saco todas las partidas siguientes a la que agarro me quedo con un
# sigma grande!
#df_TTT_h['w_std'] = df_ts_h['w_std']
#df_TTT_h['b_std'] = df_ts_h['b_std']

# Para clasificar de forma mas facil, saco las pocas partidas profesionales
df_TTT_h = df_TTT_h[~df_TTT_h['whiteRank'].str.contains('p',case=False, na=False)]
df_TTT_h = df_TTT_h[~df_TTT_h['blackRank'].str.contains('p',case=False, na=False)]
# Saco partidas que no tengan info del rango, me fijo cuantas pierdo
tot = df_TTT_h.shape[0]
df_TTT_h.dropna(axis='rows', subset=['whiteRank', 'blackRank'], inplace=True)
df_TTT_h = df_TTT_h[df_TTT_h['whiteRank'].notnull()]
df_TTT_h = df_TTT_h[df_TTT_h['blackRank'].notnull()]
print('partidas sin profesionales', tot, ' porcentaje de partidas no nulas', df_TTT_h.shape[0]*100/tot)
# Para una mejor manipulacion paso le saco la d de dan y los transofrmo en numeros
df_TTT_h['whiteRank'] = df_TTT_h['whiteRank'].apply(lambda x: x.replace("d", "") if isinstance(x, str) else x )
df_TTT_h['whiteRank'] = df_TTT_h['whiteRank'].apply(lambda x: int(x) if (isinstance(x, str)) | (isinstance(x, float))else x)
df_TTT_h['blackRank'] = df_TTT_h['blackRank'].apply(lambda x: x.replace("d", "") if isinstance(x, str) else x )
df_TTT_h['blackRank'] = df_TTT_h['blackRank'].apply(lambda x: int(x) if (isinstance(x, str)) | (isinstance(x, float)) else x)
df_TTT_h.reset_index(inplace=True)

'''
df_TTT_h['diffRank'] = df_TTT_h['whiteRank'] - df_TTT_h['blackRank']

print(df_TTT_h[df_TTT_h['komi']==0.5]['diffRank'].mean() )
print(df_TTT_h[df_TTT_h['komi']==5.5]['diffRank'].mean() )
print(df_TTT_h[df_TTT_h['komi']==6.5]['diffRank'].mean() )
print(df_TTT_h[df_TTT_h['komi']==7.5]['diffRank'].mean() )


'''
print(df_TTT_h[(df_TTT_h['blackRank'] != df_TTT_h['whiteRank']) & (df_TTT_h['handicap'] == 0)].shape[0])
# Hay que poner el beta que se uso para el fiteo de pendiente uno

rango_black = df_TTT_h['whiteRank']-df_TTT_h['blackRank']
print('rango de negro mayor a blanco ', rango_black[rango_black<=0].shape[0])
###############################################################################
########################### SIN HANDICAP por ser mismo ranking ######################################
###############################################################################
# Los organizo de partidas mas nuevas a mas viejas, entonces me quedo con las primeras
# Que serian las ultimas.
# tengo que buscar la forma de sacar la partida y solo las partidas posteriores
# de esos jugadores. y trengo que hacer esto con pandas sin iterar....

print("df_TTT_h shape", df_TTT_h.shape[0])
# me quedo solo con partidas con mismo rango
df_sameRank = df_TTT_h[df_TTT_h.whiteRank == df_TTT_h.blackRank]
print("df same rank shape", df_sameRank.shape[0])
# me quedo solo con partidas con distinto rango
df_difRank = df_TTT_h[df_TTT_h.whiteRank != df_TTT_h.blackRank]
print("df dif rank shape", df_difRank.shape[0])
players_w = {}
players_b = {}
index = []
w_mean = []
b_mean = []
w_std = []
b_std = []
black_win = []
games_id = []
handicaps = []
start = []
white = []
black = []
whiteRank = []
blackRank = []
min_std = 1.
max_games = 500
count_games = 0
index_max = 0

# ver que el index este bien.

# Al final no uso los players.... simplemente me quedo con la lista de ids
for i in reversed(df_sameRank.index):
    player1 = df_sameRank.loc[i].white
    player2 = df_sameRank.loc[i].black
    player1_std = df_sameRank.loc[i].w_std_ts
    player2_std = df_sameRank.loc[i].b_std_ts
    player1_rank = df_sameRank.loc[i].whiteRank
    player2_rank = df_sameRank.loc[i].blackRank
    handicap = df_sameRank.loc[i].handicap # deberian ser todas cero igual
    if ((player1 not in players_w) and (player2 not in players_b) and
       (handicap == 1) and (player1_std <= min_std) and
       (player2_std <= min_std)):
        print('Vuelta numero', count_games, " loops dados: ", i)
        players_w[player1] = df_sameRank.loc[i].w_mean_prior
        players_b[player2] = df_sameRank.loc[i].b_mean_prior
        # voy armando dataframe de estudio
        index.append(i)
        games_id.append(df_sameRank.loc[i].id)
        black_win.append(df_sameRank.loc[i].black_win)
        white.append(df_sameRank.loc[i].white)
        black.append(df_sameRank.loc[i].black)
        #w_mean.append(df_sameRank.loc[i].w_mean_prior)
        #b_mean.append(df_sameRank.loc[i].b_mean_prior)
        #w_std.append(df_sameRank.loc[i].w_std_prior)
        #b_std.append(df_sameRank.loc[i].b_std_prior)
        #start.append(df_sameRank.loc[i].started)
        handicaps.append(df_sameRank.loc[i].handicap)
        whiteRank.append(df_sameRank.loc[i].whiteRank)
        blackRank.append(df_sameRank.loc[i].blackRank)
        count_games += 1
    if count_games >= max_games:
        #print('Partida numero:', i, 'early date', df_sameRank.loc[i].started)
        index_max = i
        break
print('primera vuelta', len(games_id))

df = pd.DataFrame(list(zip(index, games_id, white, black,
                           black_win, handicaps, whiteRank, blackRank)),
                           columns=['index', 'games_id', 'white', 'black', 'black_win',
                                     'handicap', 'whiteRank', 'blackRank'])
print(df)
#df = pd.DataFrame(list(zip(index, games_id, white, black, w_mean, b_mean, w_std,
#                           b_std, black_win, start, handicaps, whiteRank, blackRank)),
#                           columns=['index', 'games_id', 'white', 'black', 'w_mean',
#                                    'b_mean', 'w_std', 'b_std', 'black_win',
#                                    'started', 'handicap', 'whiteRank', 'blackRank'])

# queda bien, pierdo el index
#df = df.sort_values(by=['started', 'games_id'], ascending=[True, True])
df.to_csv("../img/Datos/StudySet_sameRank.csv", index=True)

# esta ordenada bien
#df_TTT_h = df_TTT_h.sort_values(by=['started'], ascending=False)
print("df TTT filtered shape", df_TTT_h.shape[0])

# Quiero filtrar todas las partidas de un jugador posteriores a la que agarre
# voy partida por partida seleccionadas
# entonces agarro todas las partidas que uno de los jugadores aparece en partidas
# futuras a la que quiero y despues niego eso quedandome con lo contrario.
# esta mal, me esta sacando todas las paritdas

#chequear lo del indice
for i in range(0, len(index)):
    df_TTT_h = df_TTT_h[~((((df_TTT_h['white'] == white[i]) |
                        (df_TTT_h['black'] == white[i]) |
                        (df_TTT_h['white'] == black[i]) |
                        (df_TTT_h['black'] == black[i]))) &
                        (df_TTT_h.index >= index[i]))]


# saco las partidas que agarre para estudio
df_TTT_h = df_TTT_h[~df_TTT_h['id'].isin(games_id)]
print("df TTT filtered shape", df_TTT_h.shape[0])

#df_TTT_h = df_TTT_h.sort_values(by=['started', 'id'], ascending=[True, True])
#df_TTT_h = df_TTT_h.sort_values(by=['started', 'id'])
#df_TTT_h.reset_index(drop=True, inplace=True)

df_TTT_h.to_csv("../img/Datos/TrainSet_sameRank.csv", index=True)

###############################################################################
########################### CON HANDICAP ######################################
###############################################################################
# me quedo solo con partidas con mismo rango
df_difRank = df_TTT_h[df_TTT_h.whiteRank != df_TTT_h.blackRank]
print("df dif rank shape", df_difRank.shape[0])
players_w = {}
players_b = {}
index = []
w_mean = []
b_mean = []
w_std = []
b_std = []
black_win = []
games_id = []
handicaps = []
start = []
white = []
black = []
whiteRank = []
blackRank = []
min_std = 1.
max_games = 500
count_games = 0
index_max = 0

# Al final no uso los players.... simplemente me quedo con la lista de ids
# son jugadores con una diferencia considerable
for i in reversed(df_difRank.index):
    player1 = df_difRank.loc[i].white
    player2 = df_difRank.loc[i].black
    player1_std = df_difRank.loc[i].w_std_ts
    player2_std = df_difRank.loc[i].b_std_ts
    player1_rank = df_difRank.loc[i].whiteRank
    player2_rank = df_difRank.loc[i].blackRank
    handicap = df_difRank.loc[i].handicap # deberian ser todas cero igual
    if ((player1 not in players_w) and (player2 not in players_b) and
       (handicap != 1) and (player1_std <= min_std) and
       (player2_std <= min_std)):
        #print('Vuelta numero', count_games, " loops dados: ", i)
        players_w[player1] = df_difRank.loc[i].w_mean_prior
        players_b[player2] = df_difRank.loc[i].b_mean_prior
        # voy armando dataframe de estudio
        index.append(i)
        games_id.append(df_difRank.loc[i].id)
        black_win.append(df_difRank.loc[i].black_win)
        white.append(df_difRank.loc[i].white)
        black.append(df_difRank.loc[i].black)
        #w_mean.append(df_sameRank.loc[i].w_mean_prior)
        #b_mean.append(df_sameRank.loc[i].b_mean_prior)
        #w_std.append(df_sameRank.loc[i].w_std_prior)
        #b_std.append(df_sameRank.loc[i].b_std_prior)
        #start.append(df_difRank.loc[i].started)
        handicaps.append(df_difRank.loc[i].handicap)
        whiteRank.append(player1_rank)
        blackRank.append(player2_rank)
        count_games += 1
    if count_games >= max_games:
        #print('Partida numero:', i, 'early date', df_difRank.loc[i].started)
        index_max = i
        break
        break
print('segunda vuelta', len(games_id))
df = pd.DataFrame(list(zip(index, games_id, white, black,
                           black_win, handicaps, whiteRank, blackRank)),
                           columns=['index', 'games_id', 'white', 'black', 'black_win',
                                     'handicap', 'whiteRank', 'blackRank'])
#df = pd.DataFrame(list(zip(index, games_id, white, black, w_mean, b_mean, w_std,
#                           b_std, black_win, start, handicaps, whiteRank, blackRank)),
#                           columns=['index', 'games_id', 'white', 'black', 'w_mean',
#                                    'b_mean', 'w_std', 'b_std', 'black_win',
#                                    'started', 'handicap', 'whiteRank', 'blackRank'])


# queda bien
#df = df.sort_values(by=['started','games_id'], ascending=True)
df.to_csv("../img/Datos/StudySet_diffRank.csv", index=True)

# esta ordenada bien
#df_TTT_h = df_TTT_h.sort_values(by=['started'], ascending=False)
print("df TTT filtered shape", df_TTT_h.shape[0])

# Quiero filtrar todas las partidas de un jugador posteriores a la que agarre
# voy partida por partida seleccionadas
# entonces agarro todas las partidas que uno de los jugadores aparece en partidas
# futuras a la que quiero y despues niego eso quedandome con lo contrario.
# esta mal, me esta sacando todas las paritdas
for i in range(0, len(index)):
    df_TTT_h = df_TTT_h[~((((df_TTT_h['white'] == white[i]) |
                        (df_TTT_h['black'] == white[i]) |
                        (df_TTT_h['white'] == black[i]) |
                        (df_TTT_h['black'] == black[i]))) &
                        (df_TTT_h.index >= index[i]))]

# saco las partidas que agarre para estudio
df_TTT_h = df_TTT_h[~df_TTT_h['id'].isin(games_id)]
print("df TTT filtered shape", df_TTT_h.shape[0])
#df_TTT_h = df_TTT_h.sort_values(by=['started', 'id'])
#df_TTT_h.reset_index(drop=True, inplace=True)
df_TTT_h.to_csv("../img/Datos/TrainSet_diffRank.csv", index=True)
