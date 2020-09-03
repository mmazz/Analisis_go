# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 16:19:19 2020

@author: mati
"""
import json
# data = pd.read_table('a.sgf',squeeze=False , sep='\n\n', header=None)


cuenta = 2
index = 1
data = open(f'C:\Almacenamiento\Mati\GitHub\PartidasGokifu\Partida-gokifu-\{index}.sgf', 'r', encoding="utf8")
#dic = {"JugadorBlanco":1, "JugadorNegro":1,"RangoBlanco":1,"RangoNegro":1,"Ganador":1,"Fecha":1}
dic = {"JugadorBlanco":[], "JugadorNegro":[],"RangoBlanco":[],"RangoNegro":[],"Ganador":[],"Fecha":[],
       "TM":[],"EV":[],"SO":[],"Size":[],"TI":[],"Game":[]}
lista = []
def parseSGD(data):
'''
Creo que algunos archivos tiene algun enter o algo y se agrega un \n al nombre
Genera una lista con los datos que queremos.
'''

    data = data.read()
    if len(data) == 0:
        print("No hay datos")
        return
    data1 = data.split(';')
    data = data1[1].split(']')
    Jugadas = data1[2:]
    listdic = list(range(12))
    JBflag = 0
    JNflag = 0
    RNflag = 0
    RBflag = 0
    Gflag = 0
    Fechaflag = 0
    TMflag = 0
    EVflag = 0
    SOflag = 0
    SZflag = 0
    TIflag = 0
    
# Probar si funciona mejor el poner el \ antes del corchete!
    for j in range(len(data)):
        if "PW[" in data[j]:
            listdic[0] = data[j].strip('PW\[')
            JBflag = 1
        elif "PB[" in data[j]:
            listdic[1] = data[j].strip('PB\[')
            JNflag = 1
        elif "BR[" in data[j]:
            listdic[2] = data[j].strip('BR\[')
            RNflag = 1
# Puse entero para poder hacer mean, pero deberia descontar jugadores repetidos
        elif "WR[" in data[j]:
            listdic[3] = data[j].strip('WR[')
            RBflag = 1
        elif "RE[" in data[j]:
            listdic[4] = data[j].strip('RE[')
            Gflag = 1
        elif "DT[" in data[j]:
            listdic[5] = data[j].strip('DT[')
            Fechaflag = 1
        elif "TM[" in data[j]:
            listdic[6] = data[j].strip('TM[')
            TMflag = 1
        elif "EV[" in data[j]:
            listdic[7] = data[j].strip('EV[')
            EVflag = 1
        elif "SO[" in data[j]:
            listdic[8] = data[j].strip('SO[')
            SOflag = 1
        elif "SZ[" in data[j]:
            listdic[9] = data[j].strip('SZ[')
            SZflag = 1
        elif "TI[" in data[j]:
            listdic[10] = data[j].strip('TI[')
            TIflag = 1
        if JBflag == 0:  # Por si de casualidad no esta alguno de estos datos
            listdic[0] = None
        if JNflag == 0:
            listdic[1] = None
        if RNflag == 0:
            listdic[2] = None
        if RBflag == 0:
            listdic[3] = None
        if Gflag == 0:
            listdic[4] = None
        if Fechaflag == 0:
            listdic[5] = None
        if TMflag == 0:
            listdic[6] = None
        if EVflag == 0:
            listdic[7] = None
        if SOflag == 0:
            listdic[8] = None
        if SZflag == 0:
            listdic[9] = None
        if TIflag == 0:
            listdic[10] = None
        listdic[11] = Jugadas
            
    return listdic
#%%
#Conviene asi? asi no le paso al parser un dicionario qeu va creciendo
def agregadorDicSGF(dic,data):
        dic["JugadorBlanco"].append(data[0])
        dic["JugadorNegro"].append(data[1])
        dic["RangoBlanco"].append(data[2])
        dic["RangoNegro"].append(data[3])
        dic["Ganador"].append(data[4])
        dic["Fecha"].append(data[5])
        dic["TM"].append(data[6])
        dic["EV"].append(data[7])
        dic["SO"].append(data[8])
        dic["Size"].append(data[9])
        dic["TI"].append(data[10])
        dic["Game"].append(data[11])
        return dic
#%%
for index in range(1,68228):
    data = open(f'C:\Almacenamiento\Mati\GitHub\PartidasGokifu\Partida-gokifu-{index}.sgf', 'r', encoding="utf8")
    listdic = parseSGD(data)
    if type(listdic) == type(lista):
        print(index)
        agregadorDicSGF(dic,listdic)


#%%
with open('C:\Almacenamiento\Mati\GitHub\dataDic.json', "wb") as f:
    f.write(json.dumps(dic).encode("utf-8"))
#with open('C:\Almacenamiento\Mati\GitHub\dataDic.json', 'r') as fp:
#    Diccionario = json.load(fp)  
    


