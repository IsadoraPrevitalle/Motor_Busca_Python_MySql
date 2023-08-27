import mysql.connector
import numpy as np
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk

class DatabaseInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("interface de busca")
        self.host = 'localhost'
        self.user = 'root'
        self.password = '123456'
        self.database = 'targetech'
        self.create_connection()
        self.create_interface()
    
    def create_connection(self):
        self.conexao = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.conexao.cursor()

    def create_interface(self):
        #self.label = ttk.Label(self.root, text="Insira o dado que deseja encontrar:")
        #self.label.pack()

        self.entry = ttk.Entry(self.root)
        self.entry.pack()

        self.search_button = ttk.Button(self.root, text="Buscar", command=self.perform_search)
        self.search_button.pack()

        self.result_text = tk.Text(self.root)
        self.result_text.pack()

    def perform_search(self):
        valor = self.entry.get()
        buscaPal = re.split(r'\s+', valor)
        tipo_busca = str()
        mes_busca = str()
        operacao = buscaPal[0]
        linha = 0
        linha_posicao = str()
        lista = list()

        for i in buscaPal:
            var = i
            if var == 'de':
                tipo_busca = buscaPal[buscaPal.index(var) + 1]
            elif var == 'em':
                mes_busca = buscaPal[buscaPal.index(var) + 1]
            elif var == 'primeiros' or var == 'ultimos':
                linha = int(buscaPal[buscaPal.index(var) - 1])
                linha_posicao = var
        try:
            if operacao == "todos" or operacao == 'tudo':
                if mes_busca:
                    comando = f'SELECT * FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%"'
                else:
                    comando = f'SELECT * FROM targetech.fraudes'
                colunas = ["Ano", "Mês", "Total","Worm", "DOS", "Invasão", "Web", "Scan", "Fraude", "Outros"]
                self.cursor.execute(comando)
                resul = self.cursor.fetchall()

                result_text = "Resultados da Busca:\n"
                for row in resul:
                    conv = list(row)
                    lista.append(conv)
                    matriz = np.array(lista)
                df = pd.DataFrame(matriz, columns=colunas)
                result_text = df
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, result_text)

            else:
                if operacao == "soma":
                    if mes_busca:
                        comando = f'SELECT Ano, Mes, Total, SUM({tipo_busca}) FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" GROUP BY {tipo_busca}, ano, mes, total'
                    else:
                        comando = f'SELECT Ano, Mes, Total, SUM({tipo_busca}) FROM targetech.fraudes GROUP BY {tipo_busca}, ano, mes, total'  
                elif operacao == "minimo":
                    if mes_busca:
                        comando = f'SELECT Ano, Mes, Total, MIN({tipo_busca}) FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" GROUP BY {tipo_busca}, ano, mes, total'
                    else:
                        comando = f'SELECT Ano, Mes, Total, MIN({tipo_busca}) FROM targetech.fraudes GROUP BY {tipo_busca}, ano, mes, total'  
                elif operacao == "maximo":
                    if mes_busca:
                        comando = f'SELECT Ano, Mes, Total, MAX({tipo_busca}) FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" GROUP BY {tipo_busca}, ano, mes, total'
                    else:
                        comando = f'SELECT Ano, Mes, Total, MAX({tipo_busca}) FROM targetech.fraudes GROUP BY {tipo_busca}, ano, mes, total'  
                elif linha_posicao == 'primeiros':
                    if mes_busca:
                        comando = f'SELECT Ano, Mes, Total, {tipo_busca} FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" ORDER BY Ano DESC LIMIT {linha}'
                    else:
                        comando = f'SELECT Ano, Mes, Total, {tipo_busca} FROM targetech.fraudes ORDER BY Ano DESC LIMIT {linha}'
                elif linha_posicao == 'ultimos':
                    if mes_busca:
                        comando = f'SELECT Ano, Mes, Total, {tipo_busca} FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%" ORDER BY Ano ASC LIMIT {linha}'
                    else:
                        comando = f'SELECT Ano, Mes, Total, {tipo_busca} FROM targetech.fraudes ORDER BY Ano ASC LIMIT {linha}'
                elif operacao:
                    if mes_busca:
                        comando = f'SELECT Ano, Mes, Total, {operacao} FROM targetech.fraudes WHERE Mes LIKE "%{mes_busca}%"'
                    else:
                       comando = f'SELECT Ano, Mes, Total, {operacao} FROM targetech.fraudes'
                
                colunas = ["Ano", "Mês", "Total", tipo_busca or operacao]
                self.cursor.execute(comando)
                resul = self.cursor.fetchall()

                result_text = "Resultados da Busca:\n"
                for row in resul:
                    conv = list(row)
                    lista.append(conv)
                    matriz = np.array(lista)
                df = pd.DataFrame(matriz, columns=colunas)
                result_text = df
                self.result_text.delete("1.0", tk.END)
                self.result_text.insert(tk.END, result_text)

        except mysql.connector.errors.ProgrammingError as e:
            result_text = "\nDesculpe, não encontramos esse dado em nossa base. \nPor favor tente a busca com outro valor :)"
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, result_text)
    def close_connection(self):
        self.cursor.close()
        self.conexao.close()

if __name__ == "__main__":
    root = tk.Tk()
    interface = DatabaseInterface(root)
    root.mainloop()
