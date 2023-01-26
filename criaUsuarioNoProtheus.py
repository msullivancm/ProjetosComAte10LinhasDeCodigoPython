#importa modulos necessários
#Baixar o webdriver do firefox em https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-win32.zip
#descompactar o executável no caminho de instalação dos binários do python
#conda install selenium
import selenium
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

driver = webdriver.Chrome()

#options = Options()
#options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"
#driver = webdriver.Firefox(options=options, executable_path=r"C:\Program Files\Mozilla Firefox\geckodriver.exe")

#informa endereço do smartclient web e autenticação
link = f"https://s02ashm03.ferroport.com.br:8156/"
usuario = 'admin'
senha = 'P@ssw0rd2126#'
programaInicial = 'sigacfg'
ambiente = 'FRP_P12133_TESTE'
usuarioOrigem = '002351' #Número do usuário
usuarioDestino = 'acesso'
senhaDestino = 'acesso00'

driver.get(link)
time.sleep(2) 

elemento=driver.find_element_by_xpath('//*[@id="inputStartProg"]')
elemento.click()
elemento.clear()
elemento.send_keys(programaInicial)
elemento=driver.find_element_by_xpath("//input[@id='inputEnv']")
elemento.click()
elemento.clear()
elemento.send_keys(ambiente)
elemento.send_keys(Keys.TAB)
elemento=driver.find_element_by_xpath("//button[@class='button button-ok']").click()
time.sleep(10)
elemento=driver.find_element_by_xpath('//*[@id="COMP3014"]/input')
elemento.send_keys(usuario)
time.sleep(2)
elemento.send_keys(Keys.TAB)
elemento=driver.find_element_by_xpath('//*[@id="COMP3016"]/input')
elemento.click()
elemento.clear()
elemento.send_keys(senha)
driver.find_element_by_xpath('//*[@id="COMP3020"]/button').click()

time.sleep(5)
driver.find_element_by_xpath('//*[@id="COMP3036"]/button').click()
time.sleep(10)
driver.find_element_by_xpath('//*[@id="COMP3102"]/label').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="COMP3124"]/label').click()
time.sleep(10)
elemento=driver.find_element_by_xpath('//*[@id="COMP6020"]/input')
time.sleep(1)
elemento.click()
time.sleep(1)
elemento.clear()
time.sleep(2)
elemento.send_keys(usuarioOrigem)
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