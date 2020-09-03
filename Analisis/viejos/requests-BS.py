# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:48:07 2020

@author: Chuk
"""

import requests
from bs4 import BeautifulSoup

url_orig = 'http://gokifu.com/index.php'
request = requests.get(url_orig)
src = request.content
soup = BeautifulSoup(src, 'html.parser')
bloques = soup.find_all('div',{'class':"game_type"})
index = 20200 # me tiro que excedi la cantidad de request de la pagina.

def sgfFinder(url):
    request = requests.get(url)
    src = request.content
    soup = BeautifulSoup(src, 'html.parser')
    bloques = soup.find_all('div',{'class':"game_type"})
    status = request.status_code
    list_href = []
    list_sgf = []
    
    for i in range(len(bloques)):
        for j in bloques[i].find_all('a'):
            list_href.append(j['href'])
            #print(list_href)
    
    for i in range(len(list_href)):
        if '.sgf' in list_href[i]:
            list_sgf.append(list_href[i])
            #print(list_sgf)
    for i in range(len(list_sgf)):
        sgfDownloader(list_sgf[i])
        
        
    nextpage = soup.find_all('div',{'class':"nav_block"})
    for j in nextpage[0].find_all('a',string=">>"):
        list_next = j['href']
    return status, list_next 

def sgfDownloader(sgflist):
    global index
    url = sgflist
    myfile = requests.get(url)
    
    index = index+1
    open(f'/home/mati/Documents/Partidas/Partida-gokifu-{index}.sgf', 'wb').write(myfile.content)
#%%
cond = 0
list_next = url_orig + '?p=1,011'
status = 200
while status == 200: # Cambiar condicion para que llegue al final.
    cond = cond +1
    print(f"Descargando {cond}")
    status, list_next = sgfFinder(list_next)
    list_next = url_orig + list_next
    print("listo!")
