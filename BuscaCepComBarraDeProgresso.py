#!/usr/bin/env python
# coding: utf-8

#conda install -c conda-forge tqdm
#pip install requests

from tqdm import tqdm
import time
import requests 

lista_ceps = []
ceps = []

with open('ceps.txt', 'r') as arquivo:
    arquivo_lido = arquivo.read()
lista_ceps = arquivo_lido.split('\n')

for cep in tqdm(lista_ceps):
    requisicao = requests.get(f'https://cep.awesomeapi.com.br/json/{cep}')
    ceps.append(requisicao.json())

with open("ceps.json","w") as arquivojson:
    for cep in tqdm(ceps):
        arquivojson.write(f'{cep}\n')
print("arquivo json gravado")