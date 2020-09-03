# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:46:45 2020

@author: Chuk
"""
import pandas as pd
import json


def start():
    options = {
        'display': {
            'max_columns': None,
            'max_colwidth': 25,
            'expand_frame_repr': False,  # Don't wrap to multiple pages
            'max_rows': 14,
            'max_seq_items': 50,         # Max length of printed sequence
            'precision': 4,
            'show_dimensions': False
        },
        'mode': {
            'chained_assignment': None   # Controls SettingWithCopyWarning
        }
    }

    for category, option in options.items():
        for op, value in option.items():
            pd.set_option(f'{category}.{op}', value)  # Python 3.6+

if __name__ == '__main__':
    start()
    del start  # Clean up namespace in the interpreter

# ej frame = pd.DataFrame([[1,2],["Boris Yeltsin", "Mikhail Gorbachev"]],index=["row1", "row2"],columns=["column1", "column2"])
# Igual frame = pd.DataFrame({"column1": [1, "Boris Yeltsin"],<"column2": [2, "Mikhail Gorbachev"]    })
#dic = json.load(open('/home/mati/Documents/Tesis/dataDic.json'))    
#df = pd.DataFrame(dic)
    #Haciendo las cosas bien solo con pandas
df = pd.read_json('/home/mati/Documents/Tesis/dataDic.json')

# Cuando quiera guardar : df.to_filetype(filename)

#  df.iloc[0:2,:] elije por posicion, primeras 2 filas y todas las cols
# df.loc[0:2,['Size','win']] elije por label

#df[df["Size"]<20] me agarra solo las filas que cumplen esa condicion
#df.sort_values(col2,ascending=False) reordena
#df.sort_values([col1,col2],ascending=[True,False]) ordena multples cols
#df.groupby("Size").mean() #A groupby operation involves some combination of splitting the object, applying a function, and combining the results.
# df_chunk = pd.read_csv(r'../input/data.csv', chunksize=1000000)
#for chunk in df_chunk:  
    # perform data filtering 
    #chunk_filter = chunk_preprocessing(chunk)
#df[['col_1','col_5']] = df[['col_1','col_5']].astype('int32'), transforma a ese tipo de datos
# df.shape
#df.mean(axis=1) 1 para cada fila, 0 para cada columna
#si le meto argumento df un booleano me da solo los True
#plot
# df[df["platform"] == "Xbox One"]["score"].plot(kind="hist")

#df["Size"].unique()


#%%

df["Size"].unique() # vemos que elementos tiene
df.columns[:] # Vemo que columnas tengo
df["Size"].value_counts(dropna=False) # cuenta los difernetes valores en esa col
# df["Nueva_col"] = df["Size"].apply(funcion_que_quiera)
# ej df.apply(lambda x: x.dtype).head()


# Saco los Bots que aparecen explicitamente.
df = df[df['JugadorBlanco'].str.contains("Bot") != True]  
# Ver como combinar estas dos lineas
df = df[df['JugadorNegro'].str.contains("Bot") != True]
df = df.reset_index(drop=True)

#%%
'''
Pruebo generarme una Dataframe de solo nombres(pierdo la info de quien jugo con 
quien) y asi traquear jugadores individuales, OJO QUE ESTOY CONSIDERANDO LAS
PARTIDAS QUE SE JUGARON CON BOTdf2['Jugador'].strS TAMBIEN!
'''

df2 =df[["JugadorBlanco","RangoBlanco","JugadorNegro","RangoNegro","Ganador",
         "Fecha"]]
# lo estoy haciendo en mas pasos, pero agrego la info de que colo era para asi
# luego puedo ver quien gano
df2['JugadorBlanco'] = df['JugadorBlanco'].astype(str)+ ' Blancoxx'
df2['JugadorNegro'] = df['JugadorNegro'].astype(str)+' Negroxx'        
df2 = pd.concat([df2[["JugadorBlanco","RangoBlanco","Ganador","Fecha"]].rename
                 (columns = {'JugadorBlanco' :'Jugador','RangoBlanco' :'Rango'})
                 ,df2[["JugadorNegro","RangoNegro","Ganador","Fecha"]].rename
                 (columns={'JugadorNegro':'Jugador','RangoNegro':'Rango'})],
                ignore_index=True)
df2 = df2[df2['Jugador'].str.contains("Bot") != True]

#%% Aprender realmente como se hace esto de manera optima
#Quiero que la columna ganador diga si gano o perdio el jugador mirando
# el parametro que agregue, SOLO usar funciones de pandas!

#df2[df2['Jugador'].str.startswith('Blanco')][df2[df2['Jugador'].str.startswith('Blanco')]['Ganador'].str.startswith('W+',na=False)]['Ganador']=
#Selecciono solo los jugadores blancos
df2blanco = df2[df2['Jugador'].str.endswith('Blancoxx')]['Ganador'].replace(to_replace =["B+", "W+"],value =['Perdio', 'Gano'],regex=True)
df2negro = df2[df2['Jugador'].str.endswith('Negroxx')]['Ganador'].replace(to_replace =["W+", "B+"],value =['Perdio', 'Gano'],regex=True) 

# %%
df2['Ganador'] = pd.concat([df2blanco,df2negro])
# %% Claramente esta mal el parser, revisarlo!!!

df2['Jugador'] = df2['Jugador'].str.replace('Blancoxx', '')
df2['Jugador'] = df2['Jugador'].str.replace('Negroxx', '')
df2['Jugador'] = df2['Jugador'].str.replace('\nPB', '')
df2['Jugador'] = df2['Jugador'].str.replace('\nPW', '')
df2['Jugador'] = df2['Jugador'].str.replace('PB', '')
df2['Jugador'] = df2['Jugador'].str.replace('PW', '')
df2['Jugador'] = df2['Jugador'].str.replace('\[', '')

# %%
df2['Fecha'] = df2['Fecha'].str.replace('DT\[', '',regex=True)
df2['Ganador'] = df2['Ganador'].str.replace('RE\[', '')
df2 = df2.sort_values('Jugador')
df2 = df2.reset_index(drop=True)

# %%

df2.to_csv('gokifu.csv')

# %%
df3 = df2.groupby(['Jugador','Ganador'])['Ganador'].count().reset_index(name='count')



# %% Quiero un dataframe con solo los jugadores partidos jugados y ganados
df3 = df2.groupby(['Jugador']).size().reset_index(name='count')
df3 = df3.sort_values('count', ascending=False)
df3 = df3.reset_index(drop=True)

df3.groupby()
#df3['Partidas Ganadas'] = df3.groupby(['Jugador']).size().reset_index(name='count')
df3.loc[df3['count'] > 500]

df4 = df3.loc[df3['count'] > 500]

