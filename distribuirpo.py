#!/usr/bin/env python
# coding: utf-8
import os
import shutil
from datetime import datetime
from tqdm import tqdm
from six.moves import configparser as ConfigParser
""" Para gerar o executável devemos:
pip3 install pyinstaller
python -m PyInstaller --onefile distribuirpo.py"""

#atribuiçaõ de variáveis
arqConfigExist=False
try:
    VerificaIni = open('distribuirpo.ini')
    VerificaIni.close()
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
    aArqApo = cfg.get('arquivos','aArqApo').split(',')
    aChave = cfg.get('arquivos','aChave').split(',')
    aDirIni = cfg.get('destino','aDirIni').split(',')
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

    aArqApo = input("Informe o nome do arquivo APO de origem que será copiado para o destino(Se não for informado o padrão será utilizada): ")
    if aArqApo:
        pass
    else:
        aArqApo = ['tttm120.rpo']

    aChave = input("Informe o nome da chave que deverá ser alterada(Se não for informado o padrão será utilizada): ")
    if aChave:
        pass
    else:
        aChave = ['sourcepath']

    aDirIni = input("Informe o nome do diretório onde estão os INIs(Se não for informado o padrão será utilizada): ")
    if aDirIni:
        pass
    else:
        aDirIni = 'appserver'
        
#Lê o diretório onde tem os INIs e guarda
def leInis(dirInis):
    aInis=[]
    os.chdir(dirInis)
    for d in tqdm(os.listdir()):
        if d in aDirIni: 
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
    dirDataHora = datetime.now().strftime('%Y%m%d%H%M')
    dirDataHoraDestApos=f'{dirDestApo}\{dirDataHora}'
    return dirDataHoraDestApos

#Cria diretório com a data e hora atuais em cada uma das pastas de destino do Apo
def criaDirDataHoraDestAPOs(dirDataHoraDestApos):
    print(f'Criando o diretório: {dirDataHoraDestApos}')
    try:
        os.mkdir(dirDataHoraDestApos, 777)
    except OSError as err:
        return print(err)
            
#Copia o apo origem para todos os diretórios de Apo destino em sua pasta de data e hora
def copiaAPOparaDest(dirDataHoraDestApos):
    for a in aArqApo:
        origem = f'{dirOrigApo}\\{a}'
        print(f'Copiando de {origem} para {dirDataHoraDestApos}.')
        try:
            shutil.copy(origem, f'{dirDataHoraDestApos}\\{a}')  
        except OSError as err:
            return print(err)      

#Altera a linha SourcePath de cada um dos INIs para seu respectivo diretório de APO
def substCaminhoRpo(aInis,dirDataHoraDestApos,arqIni):
    aArquivo=[]
    appserverini=[]
    for d in aInis:
        ini = f'{d}\\{arqIni}'
        try: 
            print(ini)
            with open(ini,'r+') as arquivo:
                appserverini = ConfigParser.ConfigParser()
                appserverini.read(ini)
                for key in aChave:
                    for section in appserverini.sections():
                        if appserverini.has_option(section,key):
                            try: 
                                if 'custom' in key:
                                    for c in aArqApo:
                                        if 'custom' in c: 
                                            appserverini.set(section,key,f'{dirDataHoraDestApos}\{c}')
                                else: 
                                    appserverini.set(section,key,dirDataHoraDestApos)
                            except OSError as err:
                                print(err)
                appserverini.write(arquivo)
                """ gravaIni = open(ini, 'w')
                config.write(gravaIni)
                gravaIni.close() """
        except OSError as err:
            print(err)
try: 
    aInis=leInis(dirInis)
    aDirApos=leDirApos(dirDestApo)
    dirDataHoraDestApos=geraDirDataHoraDestAPOs(aDirApos)
    criaDirDataHoraDestAPOs(dirDataHoraDestApos)
    copiaAPOparaDest(dirDataHoraDestApos)
    substCaminhoRpo(aInis, dirDataHoraDestApos, arqIni)
except OSError as err:
    print(err)