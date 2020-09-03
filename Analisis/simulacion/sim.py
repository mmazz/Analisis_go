import sys
sys.path.append('/home/mati/Storage/Doctorado/Licar/licar/tesis/2020_Mazzanti/tesis/test')
import numpy as np
import random
import src as thM
from importlib import reload
reload(thM)

#Generate 5 random numbers between 10 and 30

MU = 25
SIGMA = MU/3
BETA = MU/6


def rendimiento(x, mu, sigma):
    y = 1/(sigma*(np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)
    return y


numero_partidas = 5000
Jugadores = {'pepe': 29, 'juan': 30, 'ruben': 35, 'lol': 40}
partidas = []
resultados = []
for i in range(numero_partidas):
    player1_key = random.sample(list(Jugadores.keys()), 1)[0]
    player1 = Jugadores[player1_key]
    Jugadores_pop = Jugadores.copy()
    Jugadores_pop.pop(player1_key, None)
    player2_key = random.sample(list(Jugadores_pop.keys()), 1)[0]
    player2 = Jugadores[player2_key]
    player1_rend = np.random.normal(loc=player1, scale=BETA, size=None)
    player2_rend = np.random.normal(loc=player2, scale=BETA, size=None)
    diff = player1_rend - player2_rend
    if diff > 0:
        diff = [0, 1]
    else:
        diff = [1, 0]
    partidas.append([[player1_key], [player2_key]])
    resultados.append(diff)
#print(partidas, resultados)

history = thM.History(partidas, resultados)


history.convergence()

TTT_post = history.learning_curves()

for key in Jugadores:
    t = TTT_post[key][0]
    print(key, Jugadores[key], round(t[1].mu,3))
