#!/usr/bin/python
# -*- coding: utf-8 -*-

#Para gerar o executavel devemos:
#pip3 install pyinstaller
#python -m PyInstaller --onefile apiRest.py

#Para instalar o servico, execute o seguinte comando no prompt de comando:
#sc create ".ApiRest" binpath= "C:\Users\Sullivan\source\protheus\Plano de Saude\WebService\API_REST\mobile_app\dist\apiRest.exe" DisplayName= ".ApiRest" start= auto

from flask import Flask, render_template, jsonify, request
import json
import os
from requests import Session
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth  
import requests
import json 
import xmltodict
import time

def getXml(url):
    # create response object
    r = requests.get(url = url)
    # return response content
    return r.content

def convertXml2Json(cXml):
    # read the xml file
    data_dict = xmltodict.parse(cXml)
    # generate the object using json.dumps()
    json_data = json.dumps(data_dict)
    #return jsonify(json_data)
    return json.loads(json_data)

def retornaExtratoReembolso(cChvbenf, dDtinic, dDtfina):
    url = 'https://www.caberj.com.br/wspls/WS005.apw?WSDL'
    #Variaveis preenchidas somente para teste
    if not cChvbenf and not dDtfina and not dDtinic:
        cChvbenf='00010001005290000'
        dDtinic='10/03/2023'
        dDtfina='10/03/2023'
    session = Session()
    session.auth = HTTPBasicAuth("user","password")
    transport = Transport(session=session)  
    client = Client(url,transport=transport)
    #print(client.wsdl.dump())
    with client.settings(raw_response=True):
        response = client.service.EXTRATO_REEMBOLSO(_CCHVBENF=cChvbenf, 
                                                _DDTINIC=dDtinic, 
                                                _DDTFINA=dDtfina)
        # response is now a regular requests.Response object
        assert response.status_code == 200
        assert response.content
    return response.content

def retornaDadosBeneficiarios(cLogin, cPass):
    url = 'http://10.19.1.8/ws/WS_LOGIN_BENEFICIARIO.apw?WSDL'
    session = Session()
    session.auth = HTTPBasicAuth("user","password")
    transport = Transport(session=session)  
    client = Client(url,transport=transport)
    with client.settings(raw_response=True):
        response = client.service.WS_BENEFICIARIO_LOGIN(USER_MOBILE_LOGIN_TIPO=1, 
                                                USER_MOBILE_LOGIN=cLogin, 
                                                USER_MOBILE_SENHA=cPass, 
                                                USER_MOBILE_LOGIN_ORIGEM=3)

        # response is now a regular requests.Response object
        assert response.status_code == 200
        assert response.content
    return response.content

def retornaToken():
    url = 'http://10.19.1.8:8098/rest/api/oauth2/v1/token?grant_type=password&password=P@ssw0rd2023&username=restuser'
    while True:
        try:
            request = requests.post(url, verify=False)
            if request.status_code != 201:
                return {"Mensagem": "Erro ao obter o token na rotina retornaToken"}
            jRet = request.json()
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    return jRet

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/apirestdesenv/login", methods=["POST"])
def apiRestDesenvLogin():
    return login()

@app.route("/apirestdesenv/extratoReembolso", methods=["POST"])
def apiRestDesenvExtratoReembolso():
    return extratoReembolso() 

@app.route("/extratoReembolso", methods=["POST"])
def extratoReembolso():
    cXmlRetExtratoReembolso=retornaExtratoReembolso("","","")
    cJsonRetExtratoReembolso=convertXml2Json(cXmlRetExtratoReembolso)
    cJsonRetToken = retornaToken()
    if cJsonRetToken.get("Mensagem") == None:
        return preencheJsonRetExtratoReembolso(cJsonRetExtratoReembolso,cJsonRetToken) 
    else: 
        return {"Mensagem": "Erro ao obter o token na rotina login"}

def descSituacao(cCodSituacao):
    if cCodSituacao in ['1', '2', '3', '5']:
        cDescSituacao="Solicitado"
    elif cCodSituacao in ['6']:
        cDescSituacao="Aprovado"
    else:
        cDescSituacao="Recusado"
    return cDescSituacao

def preencheJsonRetExtratoReembolso(cJson,cJToken):
    #print(cJson.keys())
    cToken = cJToken["access_token"]
    cRefresh = cJToken["refresh_token"]
    cScope = cJToken["scope"]
    cTokenType = cJToken["token_type"]
    nExpires_in = cJToken["expires_in"]
    aExtratoReembolso = cJson['soap:Envelope']['soap:Body']['EXTRATO_REEMBOLSORESPONSE']['EXTRATO_REEMBOLSORESULT']['EXTRATO']['EXTBOL']
    contratos=[]
    extrato=[]
    for i in aExtratoReembolso:
        contratos.append([
                            {"NUMEROCONTRATO":"NumeroContrato"}, 
                                {"extrato":[
                                                {"IDTIPOSERVICO":i["_CTPSVID"]}, 
                                                {"DESCRICAOTIPOSERVICO":i["_CTPSVDS"]}, 
                                                {"IDREEMBOLSO":i["_CCHVREB"]}, 
                                                {"NUMEROGUIAREEMBOLSO":i["_CCHVREB"]}, 
                                                {"NUMEROPROTOCOLO":i["_CCHVREB"]}, 
                                                {"CHAVEUNICA":i["_CMATRIC"]}, 
                                                {"NOMEBENEFICIARIO":i["_CBENNOM"]}, 
                                                {"IDTIPOBENEFICIARIO":"T"},
                                                {"SITUACAO":[
                                                                {"SITUACAO_ID":i["_NSTATID"]}, 
                                                                {"SITUACAO_DESCRICAO":descSituacao("_NSTATID")}, 
                                                                {"SITUACAO_COR":"#FF0000"}
                                                            ]   
                                                },
                                                {"DATASOLICITACAO":i["_DDTINCL"]}, 
                                                {"VALORSOLICITADO":i["_NVLAPRS"]}, 
                                                {"VALORREEMBOLSADO":i["_NVLREEM"]}
                                            ]
                                }
                        ]
                    )
    cJsonRet = {"Token": cToken, 
                "Refresh": cRefresh, 
                "Scope": cScope, 
                "TokenType": cTokenType, 
                "Expires_in": nExpires_in, 
                "contratos": ["numeroContrato",{"extrato" : contratos}]}
    return cJsonRet

@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.get_json()
        cLogin = data["login"]
        cPass = data["senha"]
    cXmlRetBeneficiario = retornaDadosBeneficiarios(cLogin, cPass)
    cJsonRetBeneficiario = convertXml2Json(cXmlRetBeneficiario)
    cJsonRetToken = retornaToken()
    if cJsonRetToken.get("Mensagem") == None:
        return preencheJsonRetBeneficiario(cJsonRetBeneficiario,cJsonRetToken) 
    else: 
        return {"Mensagem": "Erro ao obter o token na rotina login"}

def preencheJsonRetBeneficiario(cJson,cJToken):
    #print(cJson.keys())
    cToken = cJToken["access_token"]
    cRefresh = cJToken["refresh_token"]
    cScope = cJToken["scope"]
    cTokenType = cJToken["token_type"]
    nExpires_in = cJToken["expires_in"]
    cStatus = cJson['soap:Envelope']['soap:Body']['WS_BENEFICIARIO_LOGINRESPONSE']['WS_BENEFICIARIO_LOGINRESULT']['RETORNO_STATUS']
    aBeneficiario = cJson['soap:Envelope']['soap:Body']['WS_BENEFICIARIO_LOGINRESPONSE']['WS_BENEFICIARIO_LOGINRESULT']['RETORNO_DADOS']['BENEFICIARIO']
    dAcessos = cJson['soap:Envelope']['soap:Body']['WS_BENEFICIARIO_LOGINRESPONSE']['WS_BENEFICIARIO_LOGINRESULT']['RETORNO_ACESSOS']
    if aBeneficiario[0]["SEXO"] == 1:
        cCodSexo = "M"
        cDescSexo = "Masculino"
    elif aBeneficiario[0]["SEXO"] == 2:
        cCodSexo = "F"
        cDescSexo = "Feminino"
    else: 
        cCodSexo = "N"
        cDescSexo = "Não se aplica"
    if aBeneficiario[0]["BLOQUEADO"] == 'N':
        lBloqueado = False
    else:
        lBloqueado = True
    cCodECivil = 'C'
    if cCodECivil == 'C':
        cEstCivil = "Casado"
    elif cCodECivil == 'S':
        cEstCivil = "Solteiro"
    elif cCodECivil == 'V':
        cEstCivil = "Viúvo"
    elif cCodECivil == 'D':
        cEstCivil = "Divorciado"
    else:
        cEstCivil = "Não se aplica"
    dJsonRet = {}
    dJsonRet["usuarioLogado"] = {"login": aBeneficiario[0]['LOGIN'], 
                                 "chaveUnica": aBeneficiario[0]['MATRICULA'],
                                 "contato": {
                                     "email": aBeneficiario[0]['EMAIL'],
                                     "telefoneCelular": "00000000000",
                                     "telefoneFixo": "00000000000"
                                 },
                                 "esquemaCor": "esquema-premium",
                                 "integracao": {
                                                "xpto": "voluptatibus",
                                                "xyz": "quibusdam",
                                                "abcdef": 9288701
                                            }} 
    dJsonRet["beneficiarios"] = {"chaveUnica": aBeneficiario[0]["MATRICULA"], 
                                 "integracao": {
                                                "xpto": "voluptatibus",
                                                "xyz": "quibusdam",
                                                "abcdef": 9288701
                                            }, 
                                 "dadosPessoais": {
                                        "nome": aBeneficiario[0]["NOME"],
                                        "dataNascimento": aBeneficiario[0]["NASCIMENTO"],
                                        "cpf": aBeneficiario[0]["CPF"],
                                        "sexo": {
                                            "codigo": cCodSexo,
                                            "descricao": cDescSexo
                                            },  
                                        "contato": {
                                            "email": aBeneficiario[0]['EMAIL'],
                                            "telefoneCelular": "00000000000",
                                            "telefoneFixo": "00000000000"
                                            },
                                        "estadoCivil": {
                                            "codigo": cCodECivil,
                                            "descricao": cEstCivil
                                            }
                                     }, 
                                 "dadosDoContrato": {
                                            "numeroContrato": str(aBeneficiario[0]["NUMERO_CONTRATO"]),
                                            }, 
                                 "dadosDoPlano": {
                                            "beneficiario": True, 
                                            "idPlano": aBeneficiario[0]["CONVENIO_ID"],
                                            "descricao": aBeneficiario[0]["CONVENIO_DESCRICAO"],
                                            "registroAns": aBeneficiario[0]["CONVENIO_ANS"],
                                            "segmentacao": aBeneficiario[0]["CONVENIO_SEGMENTACAO"],
                                            "acomodacao": aBeneficiario[0]["CONVENIO_ACOMODACAO"],
                                            "tipoContratacao": aBeneficiario[0]["CONVENIO_TIPO_CONTRATO"],
                                            "regulamentacao": aBeneficiario[0]["CONVENIO_REGULAMENTACAO"],
                                            "abrangencia": aBeneficiario[0]["CONVENIO_ABRANGENCIA"],
                                            "modalidadeCobranca": str(aBeneficiario[0]["CONVENIO_MODALIDADE_COBRANCA"]),
                                            "padraoConforto": aBeneficiario[0]["CONVENIO_PADRAO_CONFORTO"],
                                            "participativo": True,
                                            "dataInicioVigenciaPlano": "2012-01-01",
                                            "dataFinalCpt": aBeneficiario[0]["DATA_CPT"],
                                            "matricula": aBeneficiario[0]["MATRICULA"],
                                            "matriculaAntiga": aBeneficiario[0]["MATRICULA_SIS_ANTIGO"],
                                            "matriculaFuncionario": aBeneficiario[0]["MATRICULA_FUNCIONARIO"],
                                            "tipoUsuario": {
                                                "codigo": aBeneficiario[0]["TIPO_BENEFICIARIO_ID"],
                                                "descricao": aBeneficiario[0]["TIPO_BENEFICIARIO_DESCRICAO"]
                                            },
                                            "grauParentesco": {
                                                "codigo": aBeneficiario[0]["GRAU_PARENTESCO_ID"],
                                                "descricao": aBeneficiario[0]["GRAU_PARENTESCO_DESCRICAO"]
                                            },
                                            "redeAtendimento": {
                                                "codigo": aBeneficiario[0]["CONVENIO_TIPO_REDE_ID"],
                                                "descricao": aBeneficiario[0]["CONVENIO_TIPO_REDE_DESCRICAO"]
                                            },
                                            "carencias": [aBeneficiario[0]["CONVENIO_CARENCIAS"]]
                                 },
                                 "cartao": {"modeloCartao": "modelo01",
                                            "numeroCartao": aBeneficiario[0]["MATRICULA"],
                                            "validade": aBeneficiario[0]["CARTAO_VALIDADE"],
                                            "via": int(aBeneficiario[0]["CARTAO_VIA"]),
                                            "numeroCns": aBeneficiario[0]["NUMERO_CNS"],
                                            "apresentaCartaoVirtual": True,
                                            "nomeCartao": aBeneficiario[0]["NOME"],
                                            "nomeSocialCartao": aBeneficiario[0]["NOME"],
                                            "operadoraContratada": "CAIXA DE ASSISTENCIA A SAUDE - CABERJ",
                                            "convenioAnsContratada": aBeneficiario[0]["CONVENIO_ANS"],
                                            "seed": "",
                                            "convenioAbrangenciaVerso": aBeneficiario[0]["CONVENIO_ABRANGENCIA"]
                                            },
                                "bloqueio": {
                                            "bloqueado": lBloqueado,
                                            "dataBloqueio": "2012-01-01",
                                            "motivo": str(aBeneficiario[0]["MOTIVO_BLOQUEIO"])
                                        },
                                "custom": {
                                            "xpto": "voluptatibus",
                                            "xyz": "quibusdam",
                                            "abcdef": 9288701
                                        },
                                },
    dJsonRet["contratos"] = [{
                                "descricaoContrato": aBeneficiario[0]["CONVENIO_DESCRICAO"],
                                "numeroContrato": str(aBeneficiario[0]["NUMERO_CONTRATO"]),
                                "empresaContratante": {
                                    "codigo": aBeneficiario[0]["EMPRESA_ID"],
                                    "descricao": str(aBeneficiario[0]["EMPRESA_NOME"])
                                },
                                "tipoPessoa": {
                                    "codigo": aBeneficiario[0]["TIPO_PESSOA_CONTRATANTE"][0],
                                    "descricao": aBeneficiario[0]["TIPO_PESSOA_CONTRATANTE"]
                                },
                                "tipoRelacionamento": {
                                    "codigo": "3",
                                    "descricao": "Responsavel financeio"
                                },
                                "tipoContratante": {
                                    "codigo": "3",
                                    "descricao": aBeneficiario[0]["CONVENIO_TIPO_CONTRATO"]
                                },
                                "dataInicioVigenciaContrato": "2012-01-01",
                                "dadosTitular": {
                                    "matricula": aBeneficiario[0]["MATRICULA"],
                                    "nome": aBeneficiario[0]["NOME"],
                                    "email": aBeneficiario[0]["EMAIL"],
                                    "celular": "00000000000",
                                    "telefone": "00000000000",
                                    "cpf": aBeneficiario[0]["CPF"]
                                }
                            }]
    return dJsonRet
    
# colocar o site no ar
if __name__ == "__main__":
    app.run(debug=False, 
            host='0.0.0.0', 
            port=9725,
            ssl_context=('caberj_cert.pem', 'caberj_key.key')
    )
