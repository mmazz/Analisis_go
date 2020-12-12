import csv
import pandas as pd
import os
name = os.path.basename(__file__).split(".py")[0]

dic = {"white": [], "black": [], "whiteRank": [], "blackRank": [],
        'outcome': [], "started": [], "timelimit": [], "tournament": [],
        'handicap': [], "width": [], 'komi': [], "rules": [], "id": [],
        "order": [], "numMoves": []}
lista = []
def parseSGF(data,id):# Creo que algunos archivos tiene algun enter o algo y se agrega un \n al nombre
#Genera una lista con los datos que queremos.
    #data = data.read()
    data1 = data.split(';')
    data = data1[1].split(']')

    listdic = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    JBflag = 0; JNflag = 0; RNflag = 0; RBflag = 0
    Gflag = 0; Fechaflag = 0; TMflag = 0; EVflag = 0
    HAflag = 0; SZflag = 0; KMflag = 0; RUflag = 0

    listdic[12] = id
    listdic[14] = len(data1[2:])
    for j in range(len(data)):
        if "PW[" in data[j]:
            listdic[0] = data[j].strip('\nPW[')
            JBflag = 1
        elif "PB[" in data[j]:
            listdic[1] = data[j].strip('\nPB[')
            JNflag = 1
        elif "BR[" in data[j]:
            listdic[2] = data[j].strip('\nBR[')
            RNflag = 1  # Puse entero para poder hacer mean, pero deberia descontar jugadores repetidos
        elif "WR[" in data[j]:
            listdic[3] = data[j].strip('\nWR[')
            RBflag = 1
        elif "RE[" in data[j]:
            listdic[4] = data[j].strip('\nRE[')
            if "W" in data[j].strip('\nRE['):   # ACA esta el 13
                listdic[13] = 0
            elif "B" in data[j].strip('\nRE['):
                listdic[13] = 1
            Gflag = 1
        elif "DT[" in data[j]:
            listdic[5] = data[j].strip('\nDT[')
            Fechaflag = 1
        elif "TM[" in data[j]:
            listdic[6] = data[j].strip('\nTM[')
            TMflag = 1
        elif "EV[" in data[j]:
            listdic[7] = data[j].strip('\nEV[')
            EVflag = 1
        elif "HA[" in data[j]:
            listdic[8] = data[j].strip('\nHA[')
            HAflag = 1
        elif "SZ[" in data[j]:
            listdic[9] = data[j].strip('\nSZ[')
            SZflag = 1
        elif "KM[" in data[j]:
            listdic[10] = data[j].strip('\nKM[')
            KMflag = 1
        elif "RU[" in data[j]:
            listdic[11] = data[j].strip('\nRU[')
            RUflag = 1

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
        if HAflag == 0:
            listdic[8] = None
        if SZflag == 0:
            listdic[9] = None
        if KMflag == 0:
            listdic[10] = None
        if RUflag == 0:
            listdic[11] = None
    return listdic

#Conviene asi? asi no le paso al parser un dicionario qeu va creciendo
def agregadorDicSGF(data):
    global dic
    dic["white"].append(data[0])
    dic["black"].append(data[1])
    dic["whiteRank"].append(data[2])
    dic["blackRank"].append(data[3])
    dic["outcome"].append(data[4])
    dic["started"].append(data[5])
    dic["timelimit"].append(data[6])
    dic["tournament"].append(data[7])
    dic["handicap"].append(data[8])
    dic["width"].append(data[9])
    dic["komi"].append(data[10])
    dic["rules"].append(data[11])
    dic["id"].append(data[12])
    dic["order"].append(data[13])
    dic["numMoves"].append(data[14])
#home = '/home/mati/Storage/Tesis/AnalisisGo-Tesis/crawler'
home = './'
directory = './parser'
#directory = '/home/mati/Storage/Tesis/AnalisisGo-Tesis/crawler/nuevo-intento/results'
id = 0
carpeta = 0
archivo = 0
indice = 0
partida = 0
partidaConEnter = 0
for sgf in os.scandir(directory):
    print("Archivo nuermo:", archivo, end='\r')
    archivo += 1
    partidaConEnter = 0
    with open(f'{sgf.path}', 'r', encoding="utf8") as data:
        datas = data.read().split(')')
        if partidaConEnter != 0:
            datas = datas[1:]
        partidaConEnter += 1
        for i in range(len(datas)-1):
            listdic = parseSGF(datas[i], id)
            agregadorDicSGF(listdic)
            id += 1

df = pd.DataFrame(dic)
df.to_csv(f"{home}/KGS.csv", encoding='utf-8', index=False)
df = None
dic = None
dic = {"white": [], "black": [], "whiteRank": [], "blackRank": [],
       'outcome': [], "started": [], "timelimit": [], "evento": [],
       'handicap': [], "width": [], 'komi': [], "rules": [], "id": []}
