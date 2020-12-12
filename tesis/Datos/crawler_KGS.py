# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:48:07 2020
@author: mmazz
"""

import requests
from bs4 import BeautifulSoup


# lo hago generico, pero para este caso solo voy a usar una unica pagina
def trade_spider(max_pages):
    page = 1
    while page <= max_pages:
        url = 'https://u-go.net/gamerecords-4d/'
        # aca estoy guardando todo el sourcecode
        source_code = requests.get(url)
        plain_text = source_code.text
        # necesito un objeto de BeautifulSoupfeatures="lxml"
        soup = BeautifulSoup(plain_text, "html.parser")
        # a de anker osea links
        # voy metiendome en la table hasta llegar
        for table in soup.findAll('table', {'class': 'table'}):
            for tr in table.findAll('tr'):
                for a in tr.findAll('a'):
                    myfile = a['href']
                    r = requests.get(myfile, allow_redirects=True)
                    name = myfile.replace('https://dl.u-go.net/gamerecords-4d/', '')
                    open(f'./{name}', 'wb').write(r.content)
        page += 1


trade_spider(1)
