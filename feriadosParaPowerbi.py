import datetime as dt
import requests
import pandas as pd
        
def feriados(data):
    link = f'https://api.invertexto.com/v1/holidays/{data}?token=2072|XP6Aaaz4nhBX90CT3GeEnzHxs0WBMW9J&state=rj'
    req = requests.get(link)
    return req.json()

anoini = '2018'
currentDateTime = dt.datetime.now()
anofin = currentDateTime.date().year

df = pd.DataFrame.from_dict(feriados(anoini))

for y in range(int(anoini)+1, int(anofin)+1):
    df = pd.concat([df, pd.DataFrame.from_dict(feriados(y))])

print(df)