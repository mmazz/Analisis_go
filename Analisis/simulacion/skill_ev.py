import sys
sys.path.append('/home/mati/Storage/Doctorado/Licar/licar/tesis/2020_Mazzanti/tesis/test')
import numpy as np
import random
import src as thM
import matplotlib.pyplot as plt
from importlib import reload
reload(thM)

#Generate 5 random numbers between 10 and 30

MU = 25
SIGMA = MU/3
BETA = MU/6


def rendimiento(x, mu, sigma):
    y = (1/(sigma*(np.sqrt(2*np.pi))))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


actualizacion_num_partidas = 50
valor_actualizacion = 1
numero_partidas = 500
Jugadores = {'pepe': [28, 0], 'juan': [30, 0], 'ruben': [35, 0], 'lol': [40, 0]}
partidas = []
resultados = []
Jugadores_ev = {}

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
    # actualizador de habilidad
    if Jugadores[player1_key][1] >= actualizacion_num_partidas:
        Jugadores[player1_key][0] += valor_actualizacion
        Jugadores[player1_key][1] = 0
    if Jugadores[player2_key][1] >= actualizacion_num_partidas:
        Jugadores[player2_key][0] += valor_actualizacion
        Jugadores[player2_key][1] = 0
    Jugadores_ev[player1_key].append(Jugadores[player1_key][0])
    Jugadores_ev[player2_key].append(Jugadores[player2_key][0])
    partidas.append([[player1_key], [player2_key]])
    resultados.append(diff)

mu = 25
thM.BETA = mu/6
thM.GAMMA = 0
history = thM.History(partidas, resultados)
TS_post = history.learning_curves()

# genero diccionario para meter la evolucion de skill
TS = {}
for key in Jugadores:
    TS[key] = []
# agrego la evolucion de los jugadores, loopeo entre todos los bahces
# y despues en cada bache veo que jugadores tiene y veo su posterior
for i in range(numero_partidas):
    for j in list(history.batches[i].agents):
        t = history.batches[i].posterior(j)
        TS[j].append(round(t.mu, 3))

history.convergence()
TTT_post = history.learning_curves()
TTT = {}
# veo los posteriors finales, pero a su vez ya me genero un diccionario
# para meter la evolucion de skill
for key in Jugadores:
    TTT[key] = []
    ttt = TTT_post[key][0]
    ts = TS_post[key][0]
    print(key, ': Real:', Jugadores[key][0], 'TS:', round(ts[1].mu, 3),
          'TTT:', round(ttt[1].mu, 3))

# agrego la evolucion de los jugadores, loopeo entre todos los bahces
# y despues en cada bache veo que jugadores tiene y veo su posterior
for i in range(numero_partidas):
    for j in list(history.batches[i].agents):
        t = history.batches[i].posterior(j)
        TTT[j].append(round(t.mu, 3))

# ploteo las diferentes curvas
for key in Jugadores:
    plt.plot(TS[key], label='TS')
    plt.plot(TTT[key], label='TTT')
    plt.plot(Jugadores_ev[key], label='Real')
    plt.legend()
    plt.show()
