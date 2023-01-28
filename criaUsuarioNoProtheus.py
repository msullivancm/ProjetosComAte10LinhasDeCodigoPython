#!/usr/bin/env python
# -*- coding: latin-1 -*-

#descompactar o executável no caminho de instalação dos binários do python
#conda install selenium
import selenium
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import keyring
####Necessário executar o keyring.set_password("adminprotheus","admin","senha do admin protheus")
#####Este conjunto de chave fica salvo no sistema operacional

driver = webdriver.Chrome()

#informa endereço do smartclient web e autenticação
link = f"https://s02ashm03.ferroport.com.br:8156/"
usuario = 'admin'
senha = keyring.get_password("adminprotheus", "admin")
programaInicial = 'sigacfg'
ambiente = 'FRP_P12133_TESTE'
usuarioOrigem = '002351' #Número do usuário
usuarioDestino = 'acesso'
senhaDestino = keyring.get_password("acessoprotheus", "acesso")

print(senha)
print(senhaDestino)

driver.get(link)
time.sleep(2) 

#Escreve o programa inicial
elemento=driver.find_element_by_xpath('//*[@id="inputStartProg"]')
elemento.click()
elemento.clear()
elemento.send_keys(programaInicial)
#escreve o ambiente e entra
elemento=driver.find_element_by_xpath("//input[@id='inputEnv']")
elemento.click()
elemento.clear()
elemento.send_keys(ambiente)
elemento.send_keys(Keys.TAB)
elemento=driver.find_element_by_xpath("//button[@class='button button-ok']").click()
#Escreve o usuário
time.sleep(10)
elemento=driver.find_element_by_xpath('//*[@id="COMP3014"]/input')
elemento.send_keys(usuario)
time.sleep(2)
elemento.send_keys(Keys.TAB)
#Escreve senha e entra
elemento=driver.find_element_by_xpath('//*[@id="COMP3016"]/input')
elemento.click()
elemento.clear()
elemento.send_keys(senha)
driver.find_element_by_xpath('//*[@id="COMP3020"]/button').click()
#Confirma cotação
time.sleep(5)
driver.find_element_by_xpath('//*[@id="COMP3036"]/button').click()
#Clica no menu Usuario
time.sleep(10)
driver.find_element_by_xpath('//*[@id="COMP3101"]/label').click()
#Clica no menu senha
time.sleep(10)
driver.find_element_by_xpath('//*[@id="COMP3111"]/label').click()
#Clica no menu usuários
time.sleep(5)
driver.find_element_by_xpath('//*[@id="COMP3124"]/label').click()
#Seleciona o usuário padrão origem e escreve na pesquisa
time.sleep(10)
elemento=driver.find_element_by_xpath('//*[@id="COMP6020"]/input')
time.sleep(1)
elemento.click()
time.sleep(1)
elemento.clear()
time.sleep(2)
elemento.send_keys(usuarioOrigem)
#Clica no botão de pesquisar 
time.sleep(2)
driver.find_element_by_xpath('//*[@id="COMP6021"]/button').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="COMP6059"]/button').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="CLONE6066"]').click()
time.sleep(5)
elemento=driver.find_element_by_xpath('//*[@id="COMP7681"]/input')
time.sleep(5)
elemento.send_keys(usuarioDestino)
time.sleep(5)
elemento=driver.find_element_by_xpath('//*[@id="COMP7683"]/input')
time.sleep(2)
elemento.click()
time.sleep(2)
elemento.clear()
time.sleep(2)
elemento.send_keys(senhaDestino)
time.sleep(2)
elemento=driver.find_element_by_xpath('//*[@id="COMP7684"]/input')
time.sleep(2)
elemento.click()
time.sleep(2)
elemento.clear()
time.sleep(2)
elemento.send_keys(senhaDestino)
time.sleep(3)
driver.find_element_by_xpath('//*[@id="COMP7923"]/button').click()
time.sleep(5)
driver.close()