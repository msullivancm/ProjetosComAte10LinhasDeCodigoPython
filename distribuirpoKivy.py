# -*- coding: utf-8 -*-

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from functools import partial
import requests
import os
import shutil
from datetime import datetime
from tqdm import tqdm
from six.moves import configparser as ConfigParser
from configparser import ExtendedInterpolation

class distribui():
    #atribuiçaõ de variáveis
    arqConfigExist=False
    try:
        VerificaIni = open('distribuirpo.ini')
        VerificaIni.close()
        arqConfigExist=True
        cfg = ConfigParser.ConfigParser()
        cfg.read('distribuirpo.ini')
    except:
        print('o arquivo de configuração não existe.')

    dirOrigApo = cfg.get('origem', 'dirOrigApo')
    dirDestApo = cfg.get('destino', 'dirDestApo')
    dirInis = cfg.get('arquivos','dirInis')
    arqIni = cfg.get('arquivos','arqIni')
    aArqApo = cfg.get('arquivos','aArqApo').split(',')
    aChave = cfg.get('arquivos','aChave').split(',')
    aDirIni = cfg.get('destino','aDirIni').split(',')
    aAmbiente = cfg.get('arquivos','aAmbiente').split(',')

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

class MeuApp(App):
    def build(self):
        self.layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)

        #Menu Dropdown
        self.layout.add_widget(self.create_dropdown("Moeda", ["BTC", "USD", "EUR"]))
        self.vlr = 'BTC'

        self.btn = Button(text='Pegar Cotação', size=(200, 50))
        self.btn.bind(on_press=self.pegar_cotacao)
        self.layout.add_widget(self.btn)

        self.lbl1 = Label(text='Valor Atual:', size_hint=(1.0, 1.0), halign="center", valign="middle")
        self.lbl1.text_size=(200, None)
        self.layout.add_widget(self.lbl1)

        self.lbl = Label(text='', size_hint=(1.0, 1.0), halign="center", valign="middle")
        self.lbl.text_size = (200, None)
        self.layout.add_widget(self.lbl)


        return self.layout

    def change_select(self, wid, text, *largs):
        wid.text = text
        self.vlr=text
    def open_dropdown(self, wid, drpdn, *largs):
        drpdn.open(wid)
    def create_dropdown(self, text, options):
        selection_button = Button(text=text)
        drpdn = DropDown()
        for o in options:
            btn = Button(text=o, size_hint_y=None, height=44)
            btn.bind(on_release=partial(self.change_select,
                                        selection_button,
                                        btn.text
                                        )
                     )
            btn.bind(on_release=drpdn.dismiss)
            drpdn.add_widget(btn)
        selection_button.bind(on_release=partial(self.open_dropdown,
                                                 selection_button,
                                                 drpdn
                                                 )
                              )
        return selection_button
    def printselecao(self):
        print(self.layout.mainbutton.select)
    def pegar_cotacao(self, event):
        moeda = self.vlr.upper()
        link = f"https://economia.awesomeapi.com.br/last/{moeda}-BRL"
        req = requests.get(link).json()
        valor = req[f'{moeda}BRL']['bid']
        print(valor)
        self.lbl.text = valor
        self.btn.text = "Mudou"

if __name__ == '__main__':
    MeuApp().run()
