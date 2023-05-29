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
from model.conn import *

#Reembolso - Inicio ----------------------------------------------------------
def retornaExtratoReembolso(cChvbenf, dDtinic, dDtfina):
    jsonRet = execProcedure('OMNI_SP_LISTAREEMBOLSOS', 
                            cChvbenf, 
                            dDtinic, 
                            dDtfina,
                            'NUMEROCONTRATO' ,
                            'IDTIPOSERVICO' ,
                            'DESCRICAOTIPOSERVICO' ,
                            'IDREEMBOLSO' ,
                            'NUMEROGUIAREEMBOLSO' ,
                            'NUMEROPROTOCOLO' ,
                            'CHAVEUNICA' ,
                            'NOMEBENEFICIARIO' ,  
                            'IDTIPOBENEFICIARIO' ,
                            'ID_DEBITO' ,
                            'DESCRICAO' ,
                            'COR' ,
                            'DATASOLICITACAO' ,
                            'VALORSOLICITADO' ,
                            'VALORREEMBOLSADO')
    return jsonRet

def retornaJsonFormatadoExtratoReembolso(jJson):
    cToken=retornaToken() 
    jsonRet = {}
    for i in jJson:
        jsonRet.update({
                    "contratos" : [
                                    {
                                        "numeroContrato": i["NUMEROCONTRATO"],
                                        "extrato" : [
                                                        {
                                                            "idTipoServico": i["IDTIPOSERVICO"],
                                                            "descricaoTipoServico": i["DESCRICAOTIPOSERVICO"],
                                                            "idReembolso": i["IDREEMBOLSO"],
                                                            "numeroGuiaReembolso" : i["NUMEROGUIAREEMBOLSO"],
                                                            "numeroProtocolo" : i["NUMEROPROTOCOLO"],
                                                            "chaveUnica": i["CHAVEUNICA"],
                                                            "nomeBeneficiario": i["NOMEBENEFICIARIO"],
                                                            "idTipoBeneficiario" : i["IDTIPOBENEFICIARIO"],
                                                            "situacao" : {
                                                                "id" : i["ID_DEBITO"],
                                                                "descricao" : i["DESCRICAO"],
                                                                "cor" : i["COR"]		
                                                            },
                                                            "dataSolicitacao": i["DATASOLICITACAO"],
                                                            "valorSolicitado" : i["VALORSOLICITADO"],
                                                            "valorReembolsado" : i["VALORREEMBOLSADO"]
                                                        }
                                        ]
                                    }
                                ]
                            })
    return jsonRet

#Reembolso - Fim ----------------------------------------------------------

#Beneficiario - Inicio ----------------------------------------------------------
def retornaDadosBeneficiarios(cLogin, cPass):
    #Verifica se cLogin é cpf ou matricula
    matriculaRet = ''
    query = ''
    if len(cLogin) == 11: 
        query = f"""SELECT OBTER_MATRICULA_POR_CPF('{cLogin}') as MATRICULA FROM DUAL"""
        aMatric = execQuery(query)
        matriculaRet = aMatric[0]['MATRICULA']
    elif len(cLogin) == 17:
        matriculaRet = cLogin
    print(matriculaRet)
    if matriculaRet == '':
        return {"Mensagem": "Login inválido"}  
    else:
        query = f"""Select 'OK' as AUTENTICADO from OMNI_BENEFICIARIO_LOGIN where LOGIN = '{matriculaRet}' and SENHA = '{cPass}'"""
        ret = execQuery(query)
        if ret[0]['AUTENTICADO'] == 'OK':
            print('Usuário autenticado com sucesso')
            query = f"""SELECT * FROM omni_beneficiario WHERE chave_unica = '{matriculaRet}'"""
            jJson = execQuery(query)
            return jJson
        else:
            return {"Mensagem": "Login inválido"}

#Reembolso - Fim ----------------------------------------------------------

#Carencia - Inicio ----------------------------------------------------------
def retornaDadosCarencia(cMatricula):
    query = f"""SELECT * FROM OMNI_BENEFICIARIO_CARENCIA WHERE CHAVE_UNICA = '{cMatricula}'"""
    jJson = execQuery(query)
    return jJson

def retornaJsonFormatadoCarencia(jJson):
    jsonRet = {}
    for i in jJson: 
        jsonRet.update({
                    "carencia" : [
                                    {
                                        "tipoServico": i["TIPOSERVICO"],
                                        "carencia": i["CARENCIA"]
                                    }
                                ]
                            })
    return jsonRet
#Carencia - Fim ----------------------------------------------------------

def retornaDadosLogin(cMatricula):
    query = f"""SELECT * FROM OMNI_BENEFICIARIO_LOGIN WHERE LOGIN = '{cMatricula}'"""
    jJson = execQuery(query)
    return jJson

def retornaJsonFormatadoBeneficiario(jJson):
    cJToken=retornaToken()
    cToken = cJToken["access_token"]
    cRefresh = cJToken["refresh_token"]
    cScope = cJToken["scope"]
    cTokenType = cJToken["token_type"]
    nExpires_in = cJToken["expires_in"]
    
#Cartao - Inicio ----------------------------------------------------------
def retornaDadosCartao(cMatricula):
    query = f"""SELECT * FROM OMNI_BENEFICIARIO_CARENCIA WHERE CHAVE_UNICA = '{cMatricula}'"""
    jJson = execQuery(query)
    return jJson

def retornaCartao():
    #Busca dados do cartão
    jCartao =  {
                    "cartao": {
                        "modeloCartao": "string",
                        "numeroCartao": "string",
                        "validade": "string",
                        "via": number,
                        "numeroCns": "string",
                        "apresentaCartaoVirtual": boolean,
                        "nomeCartao":"string",
                        "nomeSocialCartao":"string",
                        "operadoraContratada":"string",
                        "convenioAnsContratada":"string",
                        "seed":"string",
                        "convenioAbrangenciaVerso":"string"
                    }
                }
    return jCartao
#Cartao - Fim ----------------------------------------------------------

def retornaBloqueio():
    #Busca dados de bloqueio
    jBloqueio = {
                    "bloqueio": {
                        "bloqueado": boolean,
                        "dataBloqueio": "string",
                        "motivo": "string"
                    }
                }

def retornaCustom():
    #Busca dados customizados
    jCustom = {
                    "custom": 
                    {
                        "chave": "valor",
                        "chave2": "valor2",
                        "chave3": "valor3"
                    }    
                }

def retornaProfissionaisSaude():
    #Busca proficionais de saúde
    jProfissionaisDeSaude = [
                                {
                                    "nome": "string",
                                    "chaveProfissionalSaude": "string",
                                    "conselhoRegional": "string",
                                    "siglaConselhoRegional": "string",
                                    "estadoConselhoRegional": "string",
                                    "titulo": "string",
                                    "sexo": "string",
                                    "dataNascimento": "string",
                                    "cpf": "string",
                                    "celular": "string",
                                    "especialidades": [array-objetos],
                                    "codigoContrato": "string",
                                    "email": "string"
                                    }
                            ]

def retornaEspecialidades():
    #Busca Especialidades
    jEspecialidades = [
                        {
                            "especialidades": [
                                {
                                "cboEspecialidadeId": "string",
                                "cboEspecialidadeDescricao": "string"
                                }
                            ]
                            }
                        ]

def retornaEmpresaContratante():
    #Busca empresa contratante
    jEmpresaContratante = [
                                {
                                "empresaContratante": {
                                    "codigo": "string",
                                    "descricao": "string"
                                }
                                }
                            ]

def retornaTipoPessoa():
    #Busca tipo de pessoa
    jTipoPessoa = [
                        {
                        "tipoPessoa": {
                            "codigo": "string",
                            "descricao": "string"
                        }
                        }
                    ]

def retornaTipoRelacionamento():
    #Busca tipo relacionamento
    jTipoRelacionamento = [
                                {
                                "tipoRelacionamento": {
                                    "codigo": "string",
                                    "descricao": "string"
                                }
                                }
                            ]
def retornaTipoContratante():
    #Busca Tipo Contratante
    jTipoContratante = [
                            {
                            "tipoContratante": {
                                "codigo": "string",
                                "descricao": "string"
                            }
                            }
                        ]

def retornaTitular():
    #Busca dados Titular
    jTitular = [
                    {
                    "dadosTitular": {
                        "matricula": "string",
                        "nome": "string",
                        "email": "string",
                        "telefone": "string",
                        "celular": "string",
                        "cpf": "string"
                    }
                    }
                ]

def retornaSegmentacao():
    #Busca dados Segmentação
    jSegmentacao =  [
                        {
                        "chaveSegmentacao": "string",
                        "idSegmento": "string",
                        "descricaoSegmento": "string"
                        }
                    ]

def retornaMosia():
    #Busca Mosia módulo de chat
    jMosia = {
                "codigoAgente": "string",
                "codigoFila": "string",
                "codigoPerfil": "string"
            }

def retornaAgenteRelacionamento():
    #Busca Agente Relacionamento
    jAgenteRelacionamento = {
                                "nome": "string",
                                "telefone": "string",
                                "whatsapp": "string",
                                "email": "string",
                                "linkFoto": "string",
                                "tituloApresentacao": "string"
                            }

def retornaSexo():
    #Busca dados sexo
    jSexo =  {
                "sexo": {
                "codigo": "string",
                "descricao": "string"
                }
            }

def retornaContato():
    #Busca contato
    jContato = {
                    "contato": {
                    "email": "string",
                    "telefoneCelular": "string",
                    "telefoneFixo": "string"
                    }
                }

def retornaEstadoCivil():
    #Busca estado civil
    jEstadoCivil = {
                        "estadoCivil": {
                        "codigo": "string",
                        "descricao": "string"
                        }
                    }

def retornaDadosDoContrato():
    #Busca dados do contrato
    jDadosDoContrato = {
                            "dadosDoContrato": {
                                "numeroContrato": "string"
                                }
                        }    

def retornaDadosDoPlano():
    #Busca dados do plano
    jDadosDoPlano = {
                        "dadosDoPlano": {
                            "idPlano": "string",
                            "descricao": "string",
                            "registroAns": "string",
                            "segmentacao": "string",
                            "acomodacao": "string",
                            "tipoContratacao": "string",
                            "regulamentacao": "string",
                            "abrangencia": "string",
                            "modalidadeCobranca": "string",
                            "padraoConforto": "string",
                            "participativo": boolean,
                            "dataInicioVigenciaPlano": "string",
                            "dataFinalCpt": "string",
                            "matricula": "string",
                            "matriculaAntiga": "string",
                            "matriculaFuncionario": "string",
                            "tipoUsuario": {objeto},
                            "grauParentesco": {objeto},
                            "redeAtendimento": {objeto},
                            "carencias": [array-objetos]
                        }
                    } 

def retornaGrauParentesco():
    #Busca grau de parentesco
    jGrauParentesco =  {
                            "grauParentesco": {
                                "codigo": "string",
                                "descricao": "string"
                            }
                        }

def retornaTipoUsuario():
    #Busca tipo do usuario
    jTipoUsuario = {
                            "tipoUsuario": {
                                "codigo": "string",
                                "descricao": "string"
                            }
                    }

def retornaRedeAtendimento():
    #Busca rede de atendimento
    jRedeAtendimento =  {
                                "redeAtendimento": {
                                    "codigo": "string",
                                    "descricao": "string"
                                }
                        }

def retornaDadosPessoais():
    #Busca dados pessoais do beneficiario
    jDadosPessoais = {"beneficiarios": [
                                        {
                                            "dadosPessoais": {
                                                "nome": "string",
                                                "dataNascimento": "string",
                                                "cpf": "string",
                                                "sexo": jSexo,
                                                "contato": jContato,
                                                "estadoCivil": jEstadoCivil
                                            }
                                        }
                                        ]}

def retornaBeneficiarios():
    #Busca dados de login do beneficiario
    jBeneficiarios = {"beneficiarios": [
                                            {
                                            "chaveUnica": "string",
                                            "integracao": {objeto},
                                            "dadosPessoais": {objeto},
                                            "dadosDoContrato": {objeto},
                                            "dadosDoPlano": {objeto},
                                            "cartao": {objeto},
                                            "bloqueio": {objeto},
                                            "custom": {objeto}
                                            }
                                        ]
                        }
    return dJsonRet


# Serviço 
# Rotas da Api - Inicio ----------------------------------------------------------
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
    return extratoReembolso() 

@app.route("/listaReembolsos", methods=["POST"])
def listaReembolsos():
    data = request.json
    chaveUnica = data["chaveUnica"]
    dataInicial = data["dataInicial"]
    dataFinal = data["dataFinal"]
    jJsonRetExtratoReembolso=retornaExtratoReembolso(chaveUnica, dataInicial, dataFinal)
    jsonRet = retornaJsonFormatadoExtratoReembolso(jJsonRetExtratoReembolso) 
    return jsonify(jsonRet)


@app.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.get_json()
        cLogin = data["login"]
        cPass = data["senha"]
    jJsonRetBeneficiario = retornaDadosBeneficiarios(cLogin, cPass)
    return retornaJsonFormatadoBeneficiario(jJsonRetBeneficiario) 

# colocar o site no ar
if __name__ == "__main__":
    app.run(debug=False, 
            host='0.0.0.0', 
            port=9725,
            ssl_context=('caberj_cert.pem', 'caberj_key.key')
    )

# Rotas da Api - Fim ----------------------------------------------------------
