import calendar
import datetime as dt
import pandas as pd

anoini = 2018
anofin = dt.datetime.now().date().year
cal = calendar.Calendar(firstweekday=6).itermonthdays4(anoini,1)
caldic = {}
lista_data = []
lista_semana = []

def dia_cal(anoini, anofin):
    for a in range(anoini, anofin+1):
        for m in range(1, 12):
            cal = calendar.Calendar(firstweekday=6).itermonthdays4(a,m)

            for c in cal:
                dia=c[2]
                mes=c[1]
                ano=c[0]
                semana=calendar.day_name[c[3]]
                lista_data.append(f"{dia}/{mes}/{ano}")
                lista_semana.append(f"{semana}")
    cal_lista = zip(lista_data, lista_semana)
    #caldic = {f'"data": "{data}", "semana": "{semana}" ' for data, semana in zip(lista_data, lista_semana)}
    return cal_lista

df = pd.DataFrame(dia_cal(anoini, anofin))

print(df)