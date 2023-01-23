from workadays import workdays as wd
import datetime as dt
import requests

class Dias_uteis():
    def __init__(self, dataini, datafin):
        self.dataini = dataini
        self.datafin = datafin
    
    def get(self):
        return self.qtd_dias_uteis(self.dataini, self.datafin) 
        
    def converte_data(self,data,separador,tupla):
        if '-' in data: 
            data_lista = data.split('-')    
        elif '/' in data: 
            data_lista = data.split('/')
        if tupla:
            ano = data_lista[-1]
            mes = data_lista[-2]
            dia = data_lista[0]
            dt_data = dt.date(int(ano), int(mes), int(dia))
            return dt_data
        else: 
            data_convertida = f'{data_lista[-1]}{separador}{data_lista[-2]}{separador}{data_lista[0]}'
            return data_convertida

    def qtd_feriados_entre_datas(self, dataini, datafin):
        dataini = self.converte_data(dataini,'-', False)
        datafin = self.converte_data(datafin,'-', False)
        link = 'https://api.invertexto.com/v1/holidays/2022?token=2072|XP6Aaaz4nhBX90CT3GeEnzHxs0WBMW9J&state=rj'
        req = requests.get(link)
        qtd = 0
        for d in req.json():
            if d['date']>=dataini and d['date']<=datafin:
                qtd +=1
        return qtd

    def qtd_dias_uteis(self, dataini, datafin):
        dataini = self.converte_data(dataini, ',',True)
        datafin = self.converte_data(datafin, ',',True)
        qtd = wd.networkdays(dataini, datafin, country='BR', state='RJ')
        return qtd


print(Dias_uteis("01/01/2022","31/01/2022").get())