'''Web Scraping de páginas de restaurantes com beautifulsoup
Publicado: Ontem Propostas: 9
Preciso desenvolver um script em python que a partir do link de um restaurante
no ifood extraia um json com informações sobre os produtos e sobre os adicionais dele. 
Preciso saber sobre o produto o nome, descrição e preço dele, os adicionais do produto, 
o preço de cada uma das opções do adicional, se ele é de escolha única, 
múltipla ou somável, qual é a quantidade mínima e máxima de seleções.

https://www.ifood.com.br/delivery/campos-dos-goytacazes-rj/mcdonalds---av-dr-nilo-pecanha-cap-parque-santo-amaro/d68ad59d-4d3c-4916-9a02-77c3c976ae5f



Categoria: TI e Programação
Subcategoria: Data Science
Tamanho do projeto: Pequeño
Isso é um projeto ou uma posição de trabalho?: Um projeto
Disponibilidade requerida: Conforme necessário
colapsar'''

'''# instalar https://visualstudio.microsoft.com/pt-br/visual-cpp-build-tools/
#no instalador do visual studio, selecionar o componente MSVC 14 e instalar
from bs4 import BeautifulSoup as bs 
from lxml import etree
import requests

html = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250').content 
#strong , .secondaryInfo , .titleColumn a -> pega lista de filmes com ano e avaliação
#//*[contains(concat( " ", @class, " " ), concat( " ", "titleColumn", " " ))]

soup = bs(html, 'html.parser')
dom = etree.HTML(str(soup))

print(dom.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "titleColumn", " " ))]'))
'''

# Import Module
from bs4 import BeautifulSoup
import requests
from lxml import etree

# Website URL
URL = 'https://www.airbnb.com.br/'

# class list set
class_list = set()

# Page content from Website URL
page = requests.get( URL )

# parse html content
soup = BeautifulSoup( page.content , 'html.parser')

# get all tags
tags = {tag.name for tag in soup.find_all()}

# iterate all tags
for tag in tags:

	# find all element of tag
	for i in soup.find_all( tag ):

		# if tag has attribute of class
		if i.has_attr( "class" ):

			if len( i['class'] ) != 0:
				print(i['class'])
				class_list.add(" ".join( i['class']))

#print( class_list )

dom = etree.HTML(str(soup))
print(dom.xpath(" 	//a[@class='bn2bl2p dir dir-ltr']"))
