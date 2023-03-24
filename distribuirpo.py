#!/usr/bin/env python
# coding: utf-8
# coding: cp1252

import os
import shutil
from datetime import datetime
from tqdm import tqdm
from six.moves import configparser as ConfigParser
from configparser import ExtendedInterpolation 

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
    aAmbiente = cfg.get('arquivos','aAmbiente').split(',')
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

    aAmbiente = input("Informe o ambiente que deve ser alterado nos INIs(Se não for informado o padrão será utilizada): ")
    if aAmbiente:
        pass
    else:
        aAmbiente = 'PROD'
        
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
    for a in tqdm(aArqApo):
        origem = f'{dirOrigApo}\\{a}'
        print(f'Copiando de {origem} para {dirDataHoraDestApos}.')
        try:
            shutil.copy(origem, f'{dirDataHoraDestApos}\\{a}')  
        except OSError as err:
            return print(err)      

#Verificar estrutura do arquivo de configuração
def configToDict():
    # open the file
    file = open(r'C:\totvs\bin\appserver_05\appserver.ini')
    # create an empty dict
    sections = {}
    for line in file.readlines():
        # get rid of the newline
        line = line[:-1]
        try:
            # this will break if you have whitespace on the "blank" lines
            if line:
                # skip comment lines
                if line[0] == '#': next
                # this assumes everything starts on the first column
                if line[0] == '[':
                    # strip the brackets
                    section = line[1:-1]
                    # create a new section if it doesn't already exist
                    if not sections.has_key(section):
                        sections[section] = {}
                else:
                    # split on first the equal sign
                    (key, val) = line.split('=', 1)
                    # create the attribute as a list if it doesn't
                    # exist under the current section, this will
                    # break if there's no section set yet
                    if not sections[section].has_key(key):
                        sections[section][key] = []
                    # append the new value to the list
                    sections[section][key].append(val)
        except Exception as e:
            print(str(e) + "line:" + line)
    return sections
#Altera a linha SourcePath de cada um dos INIs para seu respectivo diretório de APO
def substCaminhoRpo(aInis,dirDataHoraDestApos,arqIni):
    aArquivo=[]
    appserverini=[]
    for d in tqdm(aInis):
        ini = f'{d}\\{arqIni}'
        try: 
            print(ini)
            with open(ini,'r') as arquivo:
                appserverini = ConfigParser.ConfigParser(allow_no_value=True, 
                                                         interpolation=ExtendedInterpolation(),
                                                         strict=False,
                                                         comment_prefixes=('#', ';'),
                                                         delimiters=('='),
                                                         defaults=None,
                                                         empty_lines_in_values=True)
                appserverini.read(ini, encoding='cp1252')
                for key in tqdm(aChave):
                    for section in tqdm(appserverini.sections()):
                        for a in aAmbiente: #Só modifica os ambientes determinados. Que são as seções do INI.
                            if appserverini.has_option(a,key):
                                try: 
                                    if 'custom' in key:
                                        for c in tqdm(aArqApo):
                                            if 'custom' in c: 
                                                appserverini.set(a,key,f'{dirDataHoraDestApos}\{c}')
                                    else: 
                                        appserverini.set(a,key,dirDataHoraDestApos)
                                except OSError as err:
                                    print(err)
                #appserverini.write(arquivo)
                with open(ini, 'w') as configfile:    # save
                    appserverini.write(configfile)
        except OSError as err:
            print(err)
try: 
    aInis=leInis(dirInis)
    aDirApos=leDirApos(dirDestApo)
    dirDataHoraDestApos=geraDirDataHoraDestAPOs(aDirApos)
    criaDirDataHoraDestAPOs(dirDataHoraDestApos)
    copiaAPOparaDest(dirDataHoraDestApos)
    substCaminhoRpo(aInis, dirDataHoraDestApos, arqIni)
    input("Tecle qualquer tecla para encerrar.")
except OSError as err:
    print(err)