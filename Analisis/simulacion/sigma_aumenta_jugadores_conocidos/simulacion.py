import sys
sys.path.append('./')
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from importlib import reload

#Generate 5 random numbers between 10 and 30

MU = 25
SIGMA = MU/3
BETA = MU/6


def rendimiento(x, mu, sigma):
    y = (1/(sigma*(np.sqrt(2*np.pi))))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


numero_partidas = 50000
Jugadores = {'pepe': [MU, 0], 'juan': [MU+1*BETA, 0], 'ruben': [MU+2*BETA, 0], 'lol': [MU+3*BETA, 0]}
partidas = []
resultados = []
Jugadores_ev = {}
jugador1 = []
jugador2 = []
player2_win = []
jugador1_real_skill = []
jugador2_real_skill = []

for key in Jugadores:
    Jugadores_ev[key] = []

for i in range(numero_partidas):
    player1_key = random.sample(list(Jugadores.keys()), 1)[0]
    player1 = Jugadores[player1_key]
    Jugadores_pop = Jugadores.copy()
    Jugadores_pop.pop(player1_key, None)
    player2_key = random.sample(list(Jugadores_pop.keys()), 1)[0]
    player2 = Jugadores[player2_key]
    player1_rend = np.random.normal(loc=player1[0], scale=BETA, size=None)
    player2_rend = np.random.normal(loc=player2[0], scale=BETA, size=None)
    diff = player1_rend - player2_rend
    if diff > 0:
        diff = [0, 1]
    else:
        diff = [1, 0]
    # flag conteo de partida de cada jugador
    Jugadores[player1_key][1] += 1
    Jugadores[player2_key][1] += 1
    Jugadores_ev[player1_key].append(Jugadores[player1_key][0])
    Jugadores_ev[player2_key].append(Jugadores[player2_key][0])
    partidas.append([[player1_key], [player2_key]])
    jugador1.append(player1_key)
    jugador1_real_skill.append(Jugadores[player1_key][0])
    jugador2.append(player2_key)
    jugador2_real_skill.append(Jugadores[player2_key][0])
    resultados.append(diff)
    player2_win.append(diff[1])

data = {'white': jugador1, 'black': jugador2, 'white_skill': jugador1_real_skill,
        'black_skill': jugador2_real_skill, 'black_win': player2_win}

df = pd.DataFrame(data)
df.to_csv("./simulacion.csv", index=False)

#gammas = [0,1, 1.5, 10, 100]
#betas = [25/5]
#for i in range(len(gammas)):
#    history = 0
#    thM.GAMMA = gammas[i]
#    thM.BETA = betas[0]
#    history = thM.History(partidas, resultados)
#
#    history.convergence()
#    t = []
#    for j in range(numero_partidas):
#        t.append(history.batches[j].evidences[0])
#    evidence_gamma = [np.sum(-np.log(t))/len(t), gammas[i]]
#    print(evidence_gamma)
#    del history
