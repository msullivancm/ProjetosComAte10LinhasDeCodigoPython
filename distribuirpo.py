#!/usr/bin/env python
# coding: utf-8
import os
import shutil
from datetime import datetime
from tqdm import tqdm
from six.moves import configparser as ConfigParser
""" Para gerar o executável devemos:
pip3 install pyinstaller
python -m PyInstaller distribuirpo.py"""

#atribuiçaõ de variáveis
arqConfigExist=False
try:
    f = open('distribuirpo.ini')
    f.close()
    arqConfigExist=True
    cfg = ConfigParser.ConfigParser()
    cfg.read('distribuirpo.ini')
except:
    print('o arquivo de configuração não existe. Logo será necessário preencher estas informações.')

if arqConfigExist: 
    dirOrigApo = cfg.get('origem', 'dirOrigApo')
    dirDestApo = cfg.get('destino', 'dirDestApo')
    dirInis = cfg.get('arquivos','dirInis')
    arqIni = cfg.get('arquivos','arqIni')
    arqApo = cfg.get('arquivos','arqApo')
else:
    dirOrigApo = input("Informe o diretório origem do APO(Se não for informado o padrão será utilizada): ")
    if dirOrigApo:
        pass
    else:
        dirOrigApo = r'C:\teste'

    dirDestApo = input("Informe o diretório de destino dos APOs(Se não for informado o padrão será utilizada): ")
    if dirDestApo:
        pass
    else: 
        dirDestApo = r'C:\apo'
    dirInis = input("Informe o diretório onde estão os binários(Se não for informado o padrão será utilizada): ")
    if dirInis:
        pass
    else:
        dirInis = r'C:\teste2'
        
    arqIni = input("Informe o nome do arquivo ini que será modificado(Se não for informado o padrão será utilizada): ")
    if arqIni:
        pass
    else:
        arqIni = 'appserver.ini'

    arqApo = input("Informe o nome do arquivo APO de origem que será copiado para o destino(Se não for informado o padrão será utilizada): ")
    if arqApo:
        pass
    else:
        arqApo = 'tttm120.rpo'

#Lê o diretório onde tem os INIs e guarda
def leInis(dirInis):
    aInis=[]
    os.chdir(dirInis)
    for d in tqdm(os.listdir()):
        aInis.append(os.path.abspath(d))
    return aInis

#Lê o diretório de destino dos APOs e guarda
def leDirApos(dirDestApo):
    aDirApos=[]
    os.chdir(dirDestApo)
    for d in tqdm(os.listdir()):
        aDirApos.append(os.path.abspath(d))
    return aDirApos
    
#Gera diretório com a data e hora atuais em cada uma das pastas de destino do Apo
def geraDirDataHoraDestAPOs(aDirApos):
    aDirDataHoraDestApos = []
    for d in aDirApos:
        dirDataHora = datetime.now().strftime('%Y%m%d%H%M')
        aDirDataHoraDestApos.append(f'{d}\{dirDataHora}')
    return aDirDataHoraDestApos

#Cria diretório com a data e hora atuais em cada uma das pastas de destino do Apo
def criaDirDataHoraDestAPOs(aDirDataHoraDestApos):
    for d in aDirDataHoraDestApos:
        print(f'Criando o diretório: {d}')
        try:
            os.mkdir(d, 777)
        except OSError as err:
            return print(err)
            
#Copia o apo origem para todos os diretórios de Apo destino em sua pasta de data e hora
def copiaAPOparaDest(aDirDataHoraDestApos):
    origem = f'{dirOrigApo}\\{arqApo}'
    for d in tqdm(aDirDataHoraDestApos):
        print(f'Copiando de {origem} para {d}.')
        try:
            shutil.copy(origem, f'{d}\\{arqApo}')  
        except OSError as err:
            return print(err)      

#Altera a linha SourcePath de cada um dos INIs para seu respectivo diretório de APO
####

try: 
    aInis=leInis(dirInis)
    aDirApos=leDirApos(dirDestApo)
    aDirDataHoraDestApos=geraDirDataHoraDestAPOs(aDirApos)
    criaDirDataHoraDestAPOs(aDirDataHoraDestApos)
    copiaAPOparaDest(aDirDataHoraDestApos)
except OSError as err:
    print(err)