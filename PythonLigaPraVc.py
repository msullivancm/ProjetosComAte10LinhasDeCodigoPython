from twilo.rest import Client

account_sid = "Seu account_sid no Twilio"
auth_token = ""
meu_numero = ""
numero_twilio = ""

cliente = Client(account_sid, token)

mensagem = """
<Response>
<Say language="pt-BR">
Ei, tudo bem? Parece que você não trabalha mais. Até ligação tá automatizada.
</Say>
</Response>
"""

ligacao = cliente.calls.create(
    to=meu_numero,
    from_=numero_twilio,
    twiml=mensagem
)
