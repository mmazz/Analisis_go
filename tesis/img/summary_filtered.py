# -*- coding: utf-8 -*-
import pandas as pd
import json

csv_name = './KGS.csv'

print("Dataframe metida")
df = pd.read_csv(csv_name)
df = df[['id', 'black', 'white', 'order', 'outcome', 'handicap', 'komi',
        'width', 'started', 'whiteRank', 'blackRank']]
print("Total: ", df.shape[0])
total = df.shape[0]
df = df[(df["width"] >= 9) & (df["width"] <= 19)]
print("Tamaño estandar: ", df.shape[0]*100/total)

# si da error, ya order es black_win, comentar esta linea
df['black_win'] = df.order
df = df[(df.black_win == 1) | (df.black_win == 0)]
print('No hay handicap negativo:', df[df.handicap < 0].shape[0])
df = df[~(df.handicap < 0)]
print("Resultado estandar: ", df.shape[0])
print("Handicap 1: ", df[df.handicap == 1.0].shape[0])
def outcomeOutput(x):
    if 'Resign' in x:
        x = 'Resign'
    elif 'Time' in x:
        x = 'Time'
    else:
        x=x
# el Nan es handicap 0/1
# ver si conviene handicap cero o uno...
df.handicap = df.handicap.apply(lambda x: x if x>=2 else 1)

#df.outcome = df.outcome.apply(lambda x: outcomeOutput(x))
df = df[['id', 'black', 'white', 'outcome', 'black_win', 'handicap', 'komi',
        'width', 'started', 'whiteRank', 'blackRank']]
# el parser tenia el error de intercambiar el rango, como ya subi base de Datos
# arreglo aca, si no sacar.
df.rename(columns={'whiteRank': 'blackRank', 'blackRank': 'whiteRank'}, inplace=True)
#df = df.sort_values(by=['started', 'id'])


#df.to_csv("./KGS_filtered.csv", index=False)
#print(df.shape)
#df = df[(df.komi==0.5)|(df.komi==5.5)|(df.komi==6.5)|(df.komi==7.5)]
print('todos los tableros',df.shape[0])
df = df[df.width==19]
print('solo 19x19',df.shape[0])
#print("Resultado estandar: ", df.shape)
#df = df.sort_values(by=['started', 'id'])
#df = df.reset_index()
#df.to_csv("./KGS_filtered_komi.csv", index=False)
print("1: ", df.shape)

print("2: ", df.shape)
df = df[~df.black.str.contains('Bot', na=False)]
df = df[~df.white.str.contains('Bot', na=False)]
df = df[~df.black.str.contains('bot', na=False)]
df = df[~df.white.str.contains('bot', na=False)]
df = df[~df.black.str.contains('BOT', na=False)]
df = df[~df.white.str.contains('BOT', na=False)]
print("3: ", df.shape)
df.reset_index(drop=True, inplace=True)
df.to_csv("./KGS_filtered.csv", index=False)
print('Partidas con mismo rango', df[df.whiteRank==df.blackRank].shape[0])
df0 = df[df.komi==0.5]
print('Partidas con mismo rango y komi 0.5', df0[df0.whiteRank==df0.blackRank].shape[0])

print("3: ", df0.shape)
print('Partidas con mismo rango y komi 0.5', df0[df0.whiteRank==df0.blackRank].shape[0])
df0.reset_index(drop=True, inplace=True)
df0.to_csv("./KGS_filtered_NoKomi.csv", index=False)
#df1 = df[(df.komi==6.5)|(df.komi==7.5)]
#print("4: ", df1.shape)
#df1 = df1.reset_index()
#df1.to_csv("./KGS_filtered_6_7Komi.csv", index=False)
