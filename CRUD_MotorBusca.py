import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='targetech',
)

cursor = conexao.cursor()

#CRUD
a = 1
while a != 0:
    valor = str(input("\nInsira o dado que deseja encontrar ou PARE para encerrar a execução: "))
    if valor == "pare":
        break
    comando = f'SELECT * FROM targetech.seguranca WHERE tipo LIKE "%{valor}%"'
    cursor.execute(comando)
    resul = cursor.fetchall()
    if resul:
        for i in resul:
            prinat("\nFraude:", i[1], "\nCidade:", i[2], "\nOcorrencias", i[4])
    else:
        print("Desculpe, não encontramos nenhum dado com esse valor em nossa base :(")
    cursor.close()
    conexao.close()