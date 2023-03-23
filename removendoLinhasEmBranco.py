arquivo='distribuirpo.py'
novoArquivo='distribuirpo2.py'
with open(arquivo, 'r') as meuArquivo:
    linhas = meuArquivo.readlines()
    novasLinhas=[]
    indice=0
    for linha in linhas:
        linha = linha.rstrip('\n')
        if linha == '':
            pass
        else: 
            novasLinhas.append(linha)
for l in novasLinhas: 
    with open(novoArquivo,'a') as gravaArquivo:
        gravaArquivo.write("\n"+l)