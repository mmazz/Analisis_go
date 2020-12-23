#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue  un  2 16:00:17 2020

@author: mati
"""
import os
name = os.path.basename(__file__).split(".py")[0]
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from scipy.optimize import curve_fit
# black_win es 1 si gano el negro.


################################################################################
######################### Valores iniciales TTT #################################
################################################################################
df_TTT_h = pd.read_csv('./TTT_H_uno.csv')

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

plt.figure(4)
t = np.linspace(0, 360, 360)
xelip = 1.5*np.cos(np.radians(t)) + 9
yelip = 0.025*np.sin(np.radians(t)) + 0.49
plt.plot(xelip, yelip, color='firebrick', linestyle='--', label='Expected zone', zorder=10)
x = np.linspace(0, 10, 1000)
z = 0.5/(1 + np.exp(-(x - 5)))

plt.plot(x, z, color='steelblue', linewidth=2, zorder=5)
plt.axvline(x=3.35, linestyle='--', linewidth=1)
plt.axvline(x=6.68, linestyle='--', linewidth=1)
plt.fill_between(x[:333], -1, 2, facecolor='steelblue', alpha=0.2)
plt.fill_between(x[334:666], -1, 2, facecolor='steelblue', alpha=0.4)
plt.fill_between(x[667:], -1, 2, facecolor='steelblue', alpha=0.6)
plt.text(1.6, 0.15, 'Stage I', fontsize=16)
plt.text(4.8, 0.15, 'Stage II', fontsize=16)
plt.text(8, 0.15, 'Stage III', fontsize=16)
plt.xlabel("Games played", fontsize=16)
plt.ylabel("Skill", fontsize=16)
plt.xlim(0, 10)
plt.ylim(0, 0.6)
plt.legend(fontsize=16)
labels = [0, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
xlabels = [0, 2, 4, 6, 8, 10]
plt.xticks(xlabels, labels)

plt.savefig('./lc_sigmoide.pdf')



df_white = df_TTT_h[['white','w_mean', 'w_mean_prior','whiteRank']]
df_black = df_TTT_h[['black','b_mean', 'b_mean_prior','blackRank']]
df_white = df_white.rename(columns={"white": "player", "w_mean": "mean",
                                    "w_mean_prior": "mean_prior",
                                    "whiteRank": "rank"})
df_black = df_black.rename(columns={"black": "player", "b_mean": "mean",
                                    "b_mean_prior": "mean_prior",
                                    "blackRank": "rank"})

frames = [df_white, df_black]
result = pd.concat(frames)
result.reset_index(drop=True, inplace=True)

print(result['mean'].min())
print(result['mean'].max())

min = 8
max = 44
step = 4
bins = []
y = 8
bins.append(y)
for i in range(9):
    y += step
    bins.append(y)
print(bins)
print(len(bins))

x = result.groupby(by='player').first()['mean_prior'].value_counts(bins=bins).index.mid.tolist()
y = result.groupby(by='player').first()['mean_prior'].value_counts(bins=bins).tolist()

for i in range(len(x)):
    x[i] = int(round(x[i]))
fig, ax = plt.subplots(1, 1)
plt.figure(0)

plt.bar(x, height=y, width=3, edgecolor='black')
xticks = [10, 14, 18, 22, 26, 30, 34, 38, 42]
xticks_dan = ['1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d']
plt.xticks(xticks, xticks_dan)
plt.xlabel(r"Rank$_0$")
plt.ylabel("Number of players")
plt.yscale('log')
plt.savefig(f'./{name}_prior_hist.pdf')


result['rank'] = result['rank'].apply(lambda x: x.replace("d", "") if isinstance(x, str) else x )
result['rank'] = result['rank'].apply(lambda x: int(x) if isinstance(x, str) else x)
x1 = result.groupby(by='player').first()['rank'].value_counts().index.tolist()
y1 = result.groupby(by='player').first()['rank'].value_counts().tolist()

fig, ax = plt.subplots(1, 1)
plt.figure(1)
plt.bar(x1, height=y1, edgecolor='black', color='firebrick')
ticks = []
for i in range(len(x1)):
    ticks.append(str(int(x1[i])) + 'd')
plt.xticks(x1, ticks)
plt.xlabel(r"Rank$_0$")
plt.ylabel("Number of players")
plt.yscale('log')
plt.savefig(f'./{name}_rank_hist.pdf')

fig, ax = plt.subplots(1, 1)
plt.figure(11)
plt.bar(x1, height=y1, edgecolor='black')
ticks = []
for i in range(len(x1)):
    ticks.append(str(int(x1[i])) + 'd')
plt.xticks(x1, ticks)
plt.xlabel(r"Rank$_0$")
plt.ylabel("Number of players")
plt.yscale('log')
plt.savefig(f'./{name}_rank_hist_blue.pdf')

print(sum(y),  sum(y1))
################################################################################
######################### Valores finales TTT #################################
################################################################################

x = result.groupby(by='player').last()['mean'].value_counts(bins=bins).index.mid.tolist()
y = result.groupby(by='player').last()['mean'].value_counts(bins=bins).tolist()

for i in range(len(x)):
    x[i] = int(round(x[i]))
fig, ax = plt.subplots(1, 1)
plt.figure(2)
plt.bar(x, height=y, width=3, edgecolor='black')
xticks = [10, 14, 18, 22, 26, 30, 34, 38, 42]
xticks_dan = ['1d', '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d']
plt.xticks(xticks, xticks_dan)
plt.xlabel(r"Rank$_0$")
plt.ylabel("Number of players")
plt.yscale('log')
plt.savefig(f'./{name}_hist_finales.pdf')

x1 = result.groupby(by='player').last()['rank'].value_counts().index.tolist()
y1 = result.groupby(by='player').last()['rank'].value_counts().tolist()

fig, ax = plt.subplots(1,1)
plt.figure(3)
plt.bar(x1, height=y1, edgecolor='black', color='firebrick')
ticks = []
for i in range(len(x1)):
    ticks.append(str(int(x1[i])) + 'd')
plt.xticks(x1,ticks)
plt.xlabel(r"Rank$_0$")
plt.ylabel("Number of players")
plt.yscale('log')
plt.savefig(f'./{name}_rank_hist_finales.pdf')

print(sum(y),  sum(y1))
################################################################################
######################### sigmoide #################################
################################################################################

# hago una elipse


'''
################################################################################
######################### curvas de aprendizaje #################################
################################################################################
#df_ts_h = pd.read_csv('./TS_datos_con_handicap_zoom.csv')
df_ts_h = pd.read_csv('./Datos/TTT_datos_con_handicap_zoom.csv')
df_ts_h = df_ts_h[['id','white','black','w_mean_prior','b_mean_prior','started','blackRank','whiteRank']]

df_ts_h =df_ts_h[df_ts_h.blackRank.str.contains('d',case=False, na=False)]

df_ts_h['whiteRank'] = df_ts_h.whiteRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
df_ts_h['blackRank'] = df_ts_h.blackRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
#df_TTT_h=df_TTT_h.drop(['blackRank', 'whiteRank'])
df_ts_h = df_ts_h[df_ts_h['whiteRank'].notnull()]
df_ts_h = df_ts_h[df_ts_h['blackRank'].notnull()]

# Ordeno los jugadores por cantidad de partidas
def law_practice_plot(*x, s=25, alpha=0.01):
    y = []
    for i in x[0]:
        y.append(s*i**alpha)
    return y


mean_rank_final = []
mean_rank_0 = []
skills_cero = []
population_cero = []
alpha = []
subpop_size = []
player_numb_games = df_ts_h[['white','black']].stack().value_counts()
fig, ax = plt.subplots()
plt.figure(5)
for n in range(10,2,-1):
    print(n)
    subplayers = player_numb_games[(player_numb_games > 2**n) & (player_numb_games < 2**(n+1))]
    subpop_size.append(len(subplayers))
    # Lista de jugadores dentro de un rango
    players = []
    for i in subplayers.index:
        players.append(i)
    # unico dataframe con los jugaores de interes en unica columna, con sus respectivas
    # medias y fecha de juego
    df_white = df_ts_h[['white','w_mean_prior','whiteRank','started']][df_ts_h.white.isin(players)]
    df_black = df_ts_h[['black','b_mean_prior','blackRank','started']][df_ts_h.black.isin(players)]
    df_white = df_white.rename(columns={"white": "player", "w_mean_prior": "mean", 'whiteRank': 'rank'})
    df_black = df_black.rename(columns={"black": "player", "b_mean_prior": "mean", 'blackRank': 'rank'})
    frames = [df_white, df_black]
    result = pd.concat(frames)
    result.reset_index(drop=True, inplace=True)
    df = pd.concat([result[result.player == p]['mean'].reset_index(drop=True) for p in players], axis=1, ignore_index=True)
    df2 = pd.concat([result[result.player == p]['rank'].reset_index(drop=True) for p in players], axis=1, ignore_index=True)
    #df = pd.concat([result[col].sort_values().reset_index(drop=True) for col in result], axis=1, ignore_index=True)
    df = df.reset_index(drop=True)
    df = df[:2**n]
    x = df.index.tolist()
    s_0 = df.mean(axis=1)[1] # dudoso... estoy agarrando el segundo valor...
    skills_cero.append(s_0)
    population_cero.append(2**n)

    def law_practice(x, alpha=0.01):
        return s_0*x**alpha

    #plt.plot(x,law_practice(x,s=df.mean(axis=1)[0]))
    mean = df.mean(axis=1).tolist()
    x.insert(0,0)
    mean.insert(0,25)
    mean_rank_0.append(df2.iloc[0,:].mean(axis=0).tolist())
    mean_rank_final.append(df2.iloc[-1,:].mean(axis=0).tolist())
    popt, pcov = curve_fit(law_practice, x, mean)
    print(popt[0], s_0)
    alpha.append(popt[0])
    plt.plot(x, mean, label=r'{} games, $\alpha =${}'.format(2**n,"{:.2e}".format(alpha[-1])))

    plt.plot(x, law_practice(x, popt[0]), linestyle='dashed')
    #plt.text(x[-1]+n, mean[-1], r'$\alpha =${}'.format(2**n,"{:.2e}".format(alpha[-1])))
print('subpop', subpop_size)
print('mean_rank_0', mean_rank_0)

print('mean_rank_final', mean_rank_final)

plt.xscale('log')
plt.ylim(25.25,27.75)
plt.xlabel("Games played", fontsize=16)
plt.ylabel("Skill", fontsize=16)
plt.ylim(25,28)
plt.legend()
#plt.show()
plt.savefig('./lc.pdf')
'''




'''
################################################################################
######################### curvas de varianza #################################
################################################################################
df_ts_h = pd.read_csv('./Datos/TS_datos_con_handicap_zoom.csv')

df_ts_h = df_ts_h[['id','white','black','w_std_prior','b_std_prior','started','blackRank','whiteRank']]
# Ordeno los jugadores por cantidad de partidas
df_ts_h =df_ts_h[df_ts_h.whiteRank.str.contains('d',case=False, na=False)]
df_ts_h =df_ts_h[df_ts_h.blackRank.str.contains('d',case=False, na=False)]

df_ts_h['whiteRank'] = df_ts_h.whiteRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
df_ts_h['blackRank'] = df_ts_h.blackRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
#df_TTT_h=df_TTT_h.drop(['blackRank', 'whiteRank'])
df_ts_h = df_ts_h[df_ts_h['whiteRank'].notnull()]
df_ts_h = df_ts_h[df_ts_h['blackRank'].notnull()]
# Ordeno los jugadores por cantidad de partidas
def law_practice_plot(*x, s=25, alpha=0.01):
    y = []
    for i in x[0]:
        y.append(s*i**alpha)
    return y

mean_rank_final = []
mean_rank_0 = []
skills_cero = []
population_cero = []
alpha = []
player_numb_games = df_ts_h[['white','black']].stack().value_counts()
fig, ax = plt.subplots()
plt.figure(5)
for n in range(10,2,-1):
    print(n)
    subplayers = player_numb_games[(player_numb_games > 2**n) & (player_numb_games < 2**(n+1))]
    # Lista de jugadores dentro de un rango
    players = []
    for i in subplayers.index:
        players.append(i)
    # unico dataframe con los jugaores de interes en unica columna, con sus respectivas
    # medias y fecha de juego
    df_white = df_ts_h[['white','w_std_prior','whiteRank','started']][df_ts_h.white.isin(players)]
    df_black = df_ts_h[['black','b_std_prior','blackRank','started']][df_ts_h.black.isin(players)]
    df_white = df_white.rename(columns={"white": "player", "w_std_prior": "mean", 'whiteRank': 'rank'})
    df_black = df_black.rename(columns={"black": "player", "b_std_prior": "mean", 'blackRank': 'rank'})
    frames = [df_white, df_black]


    result = pd.concat(frames)
    result.reset_index(drop=True, inplace=True)
    df = pd.concat([result[result.player == p]['mean'].reset_index(drop=True) for p in players], axis=1, ignore_index=True)
    df2 = pd.concat([result[result.player == p]['rank'].reset_index(drop=True) for p in players], axis=1, ignore_index=True)

    #df = pd.concat([result[col].sort_values().reset_index(drop=True) for col in result], axis=1, ignore_index=True)
    df = df.reset_index(drop=True)
    df = df[:2**n]
    x = df.index.tolist()
    mean = df.mean(axis=1).tolist()
    mean_rank_0.append(df2.loc[0].mean(axis=1).tolist())
    mean_rank_final.append(df2.loc[0].mean(axis=1).tolist())
    plt.plot(x, mean, label=r'{} games'.format(2**n))

    #plt.text(x[-1]+n, mean[-1], r'$\alpha =${}'.format(2**n,"{:.2e}".format(alpha[-1])))
plt.xscale('log')
plt.xlabel("Games played", fontsize=16)
plt.ylabel(r"$\sigma$", fontsize=16)
plt.legend()
#plt.show()
plt.savefig('./lc_sigma.pdf')
print('start', mean_rank_0)
print('final', mean_rank_final)

################################################################################
######################### Valores iniciales TS #################################
################################################################################
plt.figure(6)
plt.plot(population_cero, skills_cero, '-o')
plt.xlabel("Subpopulation", fontsize=16)
plt.ylabel(r"Skill$_0$", fontsize=16)
plt.savefig('./lc_skill.pdf')
#plt.show()
################################################################################
######################### Valores iniciales TS #################################
################################################################################
plt.figure(7)
plt.plot(population_cero, alpha, '-o')
plt.xlabel("Subpopulation", fontsize=16)
plt.ylabel(r"$\alpha$", fontsize=16)
#plt.show()
plt.savefig('./lc_alpha.pdf')
'''
'''
################################################################################
######################### curvas de aprendizaje TTT #################################
################################################################################
df_TTT_h = pd.read_csv('./TTT_datos_con_handicap_zoom.csv')

df_TTT_h = df_TTT_h[['id','white','black','w_mean','b_mean','started','blackRank','whiteRank']]
# Ordeno los jugadores por cantidad de partidas
df_TTT_h =df_TTT_h[df_TTT_h.whiteRank.str.contains('d',case=False, na=False)]
df_TTT_h =df_TTT_h[df_TTT_h.blackRank.str.contains('d',case=False, na=False)]

df_TTT_h['whiteRank'] = df_TTT_h.whiteRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
df_TTT_h['blackRank'] = df_TTT_h.blackRank.apply(lambda x: int(x.replace('d','')) if isinstance(x,str) else x)
#df_TTT_h=df_TTT_h.drop(['blackRank', 'whiteRank'])
df_TTT_h = df_TTT_h[df_TTT_h['whiteRank'].notnull()]
df_TTT_h = df_TTT_h[df_TTT_h['blackRank'].notnull()]
def law_practice_plot(*x, s=25, alpha=0.01):
    y = []
    for i in x[0]:
        y.append(s*i**alpha)
    return y


skills_cero = []
population_cero = []
mean_rank_final = []
mean_rank_0 = []
alpha = []
player_numb_games = df_TTT_h[['white','black']].stack().value_counts()
fig, ax = plt.subplots()
plt.figure(8)
for n in range(3,11):
    print(n)
    subplayers = player_numb_games[(player_numb_games > 2**n) & (player_numb_games < 2**(n+1))]
    # Lista de jugadores dentro de un rango
    players = []
    for i in subplayers.index:
        players.append(i)
    # unico dataframe con los jugaores de interes en unica columna, con sus respectivas
    # medias y fecha de juego
    df_white = df_TTT_h[['white','w_mean_prior','whiteRank','started']][df_ts_h.white.isin(players)]
    df_black = df_TTT_h[['black','b_mean_prior','blackRank','started']][df_ts_h.black.isin(players)]
    df_white = df_white.rename(columns={"white": "player", "w_mean_prior": "mean", 'whiteRank': 'rank'})
    df_black = df_black.rename(columns={"black": "player", "b_mean_prior": "mean", 'blackRank': 'rank'})
    frames = [df_white, df_black]
    result = pd.concat(frames)
    result.reset_index(drop=True, inplace=True)
    df =  pd.concat([result[result.player == p]['mean'].reset_index(drop=True) for p in players], axis=1, ignore_index=True)
    df2 = pd.concat([result[result.player == p]['rank'].reset_index(drop=True) for p in players], axis=1, ignore_index=True)

    #df = pd.concat([result[col].sort_values().reset_index(drop=True) for col in result], axis=1, ignore_index=True)
    df = df.reset_index(drop=True)
    df = df[:2**n]
    x = df.index.tolist()
    s_0 = df.mean(axis=1)[1] # dudoso... estoy agarrando el segundo valor...
    skills_cero.append(s_0)
    population_cero.append(2**n)

    def law_practice(x, alpha=0.01):
        return s_0*x**alpha

    #plt.plot(x,law_practice(x,s=df.mean(axis=1)[0]))
    mean = df.mean(axis=1).tolist()

    x.insert(0,0)
    mean.insert(0,25)
    plt.plot(x, mean,label=f'Subpopulation of {2**n}')
    popt, pcov = curve_fit(law_practice, x, mean)
    print(popt[0], s_0)
    alpha.append(popt[0])
    plt.plot(x, law_practice(x, popt[0]),linestyle='dashed')

plt.xscale('log')
plt.xlabel("Games played", fontsize=16)
plt.ylabel("Skill", fontsize=16)
plt.ylim(25,28)
plt.legend()
#plt.show()
plt.savefig('./lc_ttt.pdf')

print('start', mean_rank_0)
print('final', mean_rank_final)


'''
################################################################################
######################### ESTIMACIONES GANADAS #################################
################################################################################

'''
df_sinH = df_sinH.sort_values(by=['id'], ascending=False)
df_sinH.reset_index(drop=True, inplace=True)
players = {}
games_id = []
min_std = 1.0
max_games = 100
count_games = 0
index_max = 0
for i in df_sinH.index:
    player1 = df_sinH.loc[i].white
    player2 = df_sinH.loc[i].black
    player1_std = df_sinH.loc[i].w_std
    player2_std = df_sinH.loc[i].b_std
    player1_mean = df_sinH.loc[i].w_mean
    player2_mean = df_sinH.loc[i].b_mean
    diff = abs(player1_mean - player2_mean)
    if (diff >= beta/2) and (player1 not in players) and (player1_std <= min_std) and (player2 not in players) and (player2_std <= min_std):
        print('Vuelta numero', count_games)
        games_id.append(df_sinH.loc[i].id)
        players[player1] = df_sinH.loc[i].w_mean
        players[player2] = df_sinH.loc[i].b_mean
        count_games += 1
    if count_games >= max_games:
        print('Partida numero:', i)
        index_max = i
        break
'''
