import PySimpleGUI as sg
#pip install PySimpleGUI
import requests

def pegar_cotacao(moeda):
    moeda = moeda.upper()
    link = f"https://economia.awesomeapi.com.br/last/{moeda}-BRL"
    req = requests.get(link).json()
    valor = req[f'{moeda}BRL']['bid']
    return valor

font = ("Arial", 16)
moedas = [
    ["USD", "Dolar"],
    ["BTC", "Bitcoin"],
    ["EUR", "Euro"]
]
layout = [
    [sg.Text("Pegar Cotação da Moeda", font=font)],
    #[sg.InputText(key="nome_cotacao", font=font)],
    [sg.Combo(moedas, default_value=["USD", "Dolar"], key='combo_moedas', font=font)],
    [sg.Button("Pegar Cotação", font=font), sg.Button("Cancelar", font=font)],
    [sg.Text("", font=font, key="texto_cotacao")],
]

janela = sg.Window("Sistema de Cotações", layout)

while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED or evento == "Cancelar":
        break
    if evento == "Pegar Cotação":
        codigo_cotacao = valores["combo_moedas"][0]
        cotacao = pegar_cotacao(codigo_cotacao)
        janela["texto_cotacao"].update(f"A cotação do {codigo_cotacao} é de R${cotacao}")

janela.close()