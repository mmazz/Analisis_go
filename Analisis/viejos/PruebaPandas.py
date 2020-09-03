#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 16:19:19 2020

@author: mati
"""
import pandas as pd

#data = pd.read_table('a.sgf',squeeze=False , sep='\n\n', header=None)

JugadorBlanco = []
JugadorNegro = []
RangoBlanco = []
RangoNegro = []
Ganador = []
Fecha = []

cuenta = 2
for i in range(270):

    data = open(('kgs-19-2019-04-new/2019-04-01-{}.sgf').format(cuenta), 'r')
<<<<<<< HEAD
    cuenta = cuenta + 1  # Quizas mejorar esto, ya que hay mas archivos con otros nombres
=======
    cuenta = cuenta + 1# Quizas mejorar esto, ya que hay mas archivos con otros nombres
>>>>>>> 594d90d535f59125d126f418ffcd1d2c88f1a820
    data = data.read()
    data = data.split()

    JBflag = 0
    JNflag = 0
    RNflag = 0
    RBflag = 0
    Gflag = 0
    Fechaflag = 0

    for j in range(len(data)):
        if "PW[" in data[j]:
            JugadorBlanco.append(data[j].strip('PW[]'))
            JBflag = 1

        elif "PB[" in data[j]:
            JugadorNegro.append(data[j].strip('PB[]'))
            JNflag = 1

        elif "BR[" in data[j]:
            RangoNegro.append(int(data[j].strip('BR[d]')))
            RNflag = 1  # Puse entero para poder hacer mean, pero deberia descontar jugadores repetidos

        elif "WR[" in data[j]:
            RangoBlanco.append(int(data[j].strip('WR[d]')))
            RBflag = 1

        elif "RE[" in data[j]:
            Ganador.append(data[j].strip('RE[]'))

            Gflag = 1
        elif "DT[" in data[j]:
            Fecha.append(data[j].strip('DT[]'))

            Fechaflag = 1

    if JBflag == 0:  # Por si de casualidad no esta alguno de estos datos
        JugadorBlanco.append(None)
    if JNflag == 0:
        JugadorNegro.append(None)
    if RNflag == 0:
        RangoNegro.append(None)
    if RBflag == 0:
        RangoBlanco.append(None)
    if Gflag == 0:
        Ganador.append(None)
    if Fechaflag == 0:
        Fecha.append(None)


Datas = {'Nombre Blanco': JugadorBlanco, 'Nombre Negro': JugadorNegro,
         "Rango del Blanco": RangoBlanco, 'Rango del Negro': RangoNegro,
         "Ganador": Ganador, "Fecha": Fecha}

df = pd.DataFrame(Datas)

df = df[df['Nombre Blanco'].str.contains("Bot") != True]  # Ver como combinar estas dos lineas

df = df[df['Nombre Negro'].str.contains("Bot") != True]
df = df.reset_index(drop=True)

# Pruebo generarme una Dataframe de solo nombres(pierdo la info de quien jugo con quien) y asi
# traquear jugadores individuales, OJO QUE ESTOY CONSIDERANDO LAS PARTIDAS QUE SE JUGARON CON BOTS TAMBIEN!
Jugadores = JugadorBlanco + JugadorNegro
Fechas2 = Fecha + Fecha
Rango2 = RangoBlanco + RangoNegro


Datas2 = {"Jugadores": Jugadores, "Rango": Rango2, "Fecha": Fechas2}
df2 = pd.DataFrame(Datas2)

df2 = df2[df2['Jugadores'].str.contains("Bot") != True]
df2 = df2.sort_values('Jugadores')
df2 = df2.reset_index(drop=True)

# Otro en el cual solo me quedo con cada jugador y la cantidad de partias jugadas
df3 = df2["Jugadores"].value_counts().rename_axis('Jugadores').reset_index(name='No: de partidas')
df3 = df3.sort_values('No: de partidas',  ascending=False)
df3 = df3.reset_index(drop=True)
# print(df)
print(df2)
print(df3)
