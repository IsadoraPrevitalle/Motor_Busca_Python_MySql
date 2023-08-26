#Importando bibliotecas
import mysql.connector                                                                                      #Conexão com o banco de dados
import re                                                                                                   #Expressões regulares para texto
import numpy as np                                                                                          #Manipulação de matrizes 
import pandas as pd                                                                                         #Manipulação de dataframe

#Conexão com MySQL
conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='targetech',
)

#Declaração do cursor - responsavel pela busca linha a linha no BD
cursor = conexao.cursor()

#                                                              #Entrada e tratamento de dados do usuario
#Dados para pesquisa                                                                
valor = str(input("\nInsira o dado que deseja encontrar: "))

#declaração de variaveis que auxiliará no tratamento dos dados de entrada
buscaPal = re.split(r'\s+',valor)                                                                           #Divide o texto em palavras
tipo_busca = str()                                                                                          #Variavel do tipo da busca 
mes_busca = str()                                                                                           #Varivel do periodo de busca
operacao = buscaPal[0]                                                                                      #Operações de busca
linha = int()                                                                                               #Varivel de quantidade de busca
linha_posicao = str()                                                                                       #variavel de ordem da busca
lista = list()                                                                                              #Declaracao de lista
cont = 0

#Busca de expressões na frase - locação nas variaveis 
for i in buscaPal:
    var = i
    if var == 'de':
        tipo_busca = buscaPal[cont+1]
    elif var == 'em':
        mes_busca = buscaPal[cont+1]
    elif var == 'primeiros' or var == 'ultimos':
        linha = int(buscaPal[cont-1])
        linha_posicao = var
    cont += 1

#                                                                    #Buscas no banco de dados
#Todos os registros em um determinado mês                                                                         
if operacao == "todos" or operacao == 'tudo':
    comando = f'SELECT * FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%"'
    colunas = ["Ano", "Mês", "Total","Worm", "DOS", "Invasão", "Web", "Scan", "Fraude", "Outros"]
    cursor.execute(comando)
    resul = cursor.fetchall()
    #loop para exibição do resultado em uma matriz
    for i in resul:
        conv = list(i)
        lista.append(conv)
    matriz = np.array(lista)
    #Transformação da matriz em cvs
    df = pd.DataFrame(matriz, columns=colunas)
    print("\nResultados da Busca:\n")
    print(df.head())
    cursor.close()
    conexao.close()
#Buscas especificas
else:
    #Soma de um tipo de registros em um determinado mês nos anos de 2010 a 2019
    #                                                                                                                     #"Soma de Tipo_registro em mes_busca"
    if operacao == "soma":
        comando = f'SELECT Ano, Mes, Total, SUM({tipo_busca}) FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" GROUP BY {tipo_busca}, ano, mes, total'
    #Menor valor de um tipo de registro em um determinado mês nos anos de 2010 a 2019
    #                                                                                                                   #"Minimo de Tipo_registro em mes_busca"
    elif operacao == "minimo":
        comando = f'SELECT Ano, Mes, Total, MIN({tipo_busca}) FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" GROUP BY {tipo_busca}, ano, mes, total'
    #Maior valor de um tipo de registro em um determinado mês nos anos de 2010 a 2019
    #                                                                                                                   #"Maximo de Tipo_registro em mes_busca"
    elif operacao == "maximo":
        comando = f'SELECT Ano, Mes, Total, MAX({tipo_busca}) FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" GROUP BY {tipo_busca}, ano, mes, total'
    #Quntidade de registros nos últimos anos de um tipo em um determinado mês no periodo dos anos de 2010 a 2019- 
    #                                                                                                    #"3 primeiros_registros de Tipo_registro em mes_busca"
    elif linha_posicao == 'primeiros':
        comando = f'SELECT Ano, Mes, Total, {tipo_busca} FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" ORDER BY Ano desc LIMIT {linha}'
    #Quntidade de registros nos primeiros anos de um tipo em um determinado mês no periodo dos anos de 2010 a 2019- 
    #                                                                                                      #"3 ultimos_registros de Tipo_registro em mes_busca"
    elif linha_posicao == 'ultimos':
        comando = f'SELECT Ano, Mes, Total, {tipo_busca} FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" ORDER BY Ano asc LIMIT {linha}'
    #Quntidade de registros de um tipo em um determinado mês no periodo dos anos de 2010 a 2019- 
    #                                                                                                          #"Todos_registros de Tipo_registro em mes_busca"
    else:
        comando = f'SELECT Ano, Mes, Total, {tipo_busca} FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%"'
    colunas = ["Ano", "Mês", "Total", tipo_busca]
    cursor.execute(comando)
    resul = cursor.fetchall()
    #loop para exibição do resultado em uma matriz
    for i in resul:
        conv = list(i)
        lista.append(conv)
    matriz = np.array(lista)
    #Transformação da matriz em cvs
    df = pd.DataFrame(matriz, columns=colunas)
    print("\nResultados da Busca:\n")
    print(df)
    cursor.close()
    conexao.close()
