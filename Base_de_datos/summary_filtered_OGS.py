# -*- coding: utf-8 -*-
import pandas as pd
import sys
import json
import numpy as np
sys.path.append('../software/')

csv_name = '/home/mati/Storage/Tesis/AnalisisGo-Tesis/DatosPurificados/summary.csv'

print("Dataframe metida")
df = pd.read_csv(csv_name)
df = df[['id', 'black', 'white', 'order', 'outcome', 'handicap', 'komi', 'width', 'height', 'annulled', 'ranked', 'started', 'ended']]

filtered = {}
##%% Selecciono las columnas que quiero y las filas con ciertas restricciones
filtered['Annulled'] = sum(df.annulled != False)
df = df[df.annulled == False]
filtered['Outcomes'] = sum(~((df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point'))))
df = df[(df.outcome == 'Resignation') | (df.outcome == 'Timeout') | (df.outcome.str.contains(' point'))]
filtered['Squared'] = sum(df.height!=df.width)
df = df[df.height==df.width]
filtered['Width'] = sum(~((df["width"] >= 9) & (df["width"] <=19)))
df = df[(df["width"] >= 9) & (df["width"] <=19)]
filtered['Order'] = sum(~((df.order != "(0, 0)") & (df.order != "(1, 1)")))
df = df[(df.order == "(0, 1)") | (df.order == "(1, 0)")]#np.sum(df.order == "(0, 0)")
df = df[(df.handicap >= 0)]#np.sum(df.order == "(0, 0)")
# Hago una columna con los puntos de las partidas ganadas como tal
replace_values = {' points': '', ' point': '', 'Resignation': None,'Timeout': None}
# Hago Float los puntos
df['points'] = df.outcome.replace(replace_values, regex=True)
df.points = df.points.map(lambda x: float(x) if isinstance(x, str) else None)
#df.outcome[df.outcome.str.contains(' point', na=False)] = "Points"
replace_values = {' point': 'Points'}
df['outcome'] = df.outcome.replace(replace_values, regex=True)

df["black_win"] = df.order.map(lambda x: 1 if x[1] == '1' else 0)
#df['black_win_not_komi'] = df[['outcome', 'komi', 'black_win', 'points']].apply(lambda x: np.sign((2*x['black_win']-1)*x['points']+x['komi']) if x['outcome'].str.contains(' point') else x['black_win'], axis=1)

#df['black_win_not_komi'] = df.outcome.str.contains('Points').apply(lambda x: np.sign((2*df.black_win-1)*df.points+df.komi))
df['black_win_not_komi'] = df[['outcome', 'komi', 'black_win', 'points']].apply(lambda x: np.sign((2*x['black_win']-1)*x['points']+x['komi']) if x['outcome']=='Points' else x['black_win'],axis=1)
df['black_win_not_komi'] = df['black_win_not_komi'].apply(lambda x: 1 if x == 1 else 0)
# si agarra todos, tambien esta agarrando los que no son por puntos, entonces agasrra nones?

#df['points_not_komi'] = df[['points', 'komi', 'black_win_not_komi']].apply(lambda x: x['points']+x['komi'] if x['black_win_not_komi'] == 1 else x['points']-x['komi'] , axis=1)
def func(vec):
    if vec[3] == 'Points':
        if vec[2] == 1:
            y = vec[0] + vec[1]
        else:
            y = vec[0] - vec[1]
    else:
        y = None
    return y

df['points_not_komi'] = df[['points', 'komi', 'black_win_not_komi', 'outcome']].apply(func, axis=1)

df = df[['id', 'black', 'white', 'outcome', 'black_win', 'black_win_not_komi', 'handicap', 'komi', 'width', 'points', 'ranked', 'started', 'ended', 'points_not_komi']]
# Ordeno
df.sort_values(by=['ended', 'started', 'id'])

# Escribo los
with open('/home/mati/Storage/Tesis/handicap/Mati/DatosPurificados/filtered.json', 'w') as file:
     file.write(json.dumps(filtered)) # use `json.loads` to do the reverse

df = df.reset_index()
df.to_csv("/home/mati/Storage/Tesis/handicap/Mati/DatosPurificados/summary_filtered_handicapPositive.csv", index=False)
