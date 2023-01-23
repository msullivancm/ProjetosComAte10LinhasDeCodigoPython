import requests
import pandas as pd
import datetime

def feriados(ano):
    link = f'https://api.invertexto.com/v1/holidays/{ano}?token=2072|XP6Aaaz4nhBX90CT3GeEnzHxs0WBMW9J&state=rj'
    req = requests.get(link)
    return req.json()

anoini = 2018
anofim = datetime.date.today().year + 1
df = pd.DataFrame.from_dict(feriados(anoini-1))

for ano in range(anoini, anofim):
    #df.append(pd.DataFrame.from_dict(feriados(ano)))
    df = pd.concat([df, pd.DataFrame.from_dict(feriados(ano))])

print(df)