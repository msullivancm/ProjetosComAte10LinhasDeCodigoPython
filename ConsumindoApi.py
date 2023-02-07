import requests
import locale

def moeda(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor = locale.currency(valor, grouping=True, symbol=None)
    return valor

link = "https://economia.awesomeapi.com.br/last/BTC-BRL"

QuantoTenhoEmBitcoins = 0.02266523 
print(f'Tennho {QuantoTenhoEmBitcoins} na minha carteira digital.')

req = requests.get(link)

btcEmreais = float(req.json()['BTCBRL']['bid'])
print(f'Valor do Bitcoin em reais na cotação de hoje R${moeda(btcEmreais)}')

QuantoTenhoEmReais = QuantoTenhoEmBitcoins * btcEmreais

print(f'Eu tenho R${moeda(QuantoTenhoEmReais)} Reais na minha carteira digital')

      