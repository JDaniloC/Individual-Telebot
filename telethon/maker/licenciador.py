from tkinter import *
from cryptography.fernet import Fernet
from tkinter import messagebox
from os import path, environ
import json

KEY = b'5oa6VUCRinbN50aH5XT7gOfrbdCeOaEUembWDV3EIW4='

class Gerador(Frame):
    def __init__(self, janela, timestamp, atual, total):
        super().__init__(janela)        

        for var in ('HOME', 'USERPROFILE', 'HOMEPATH', 'HOMEDRIVE'):
            if environ.get(var) != None:
                self.caminho = environ.get(var)
                try:
                    with open(self.caminho + "/k", "w") as file:
                        file.write("")
                    self.caminho += "/HNRSAGL"
                    break
                except:
                    pass

        self.pirateado = False
        self.janela = janela
        self.timestamp = timestamp
        self.atual = atual
        self.total = total
        if atual == total:
            messagebox.showwarning(
                "LICENCA", "Chegou no limite de licenças compre um novo limite.")
        self.conferir_integridade()

        self.pack(fill = X, padx = 10, pady = 10)
        self.widgets()

    def conferir_integridade(self):
        '''
        Confere se no arquivo de integridade essa licença já não foi usada.
        '''
        try:
            adicionar = False
            if path.exists(self.caminho):
                with open(self.caminho, "r+") as file:
                    licencas = json.load(file)
                    if self.timestamp in licencas:
                        if licencas[self.timestamp] != self.atual:
                            messagebox.showerror(
                                "PIRATA", 
                                "Incongruência no arquivo de licença. Peça outro.")
                            self.pirateado = True
                    else:
                        adicionar = True
                if adicionar:
                    with open(self.caminho, "w") as file:
                        licencas.update({self.timestamp: self.atual})
                        file.write("")
                        json.dump(licencas, file)
            else:
                with open(self.caminho, "w") as file:
                    json.dump({self.timestamp: self.atual}, file)
        except Exception as e:
            print(e)

    def widgets(self):
        '''
        Instancia todos os widgets e suas respectivas variáveis
        '''
        self.titulos = {
            "dia": IntVar(value = 1), 
            "mês": IntVar(value = 1),
            "ano": IntVar(value = 2021),
            "hora": IntVar(value = 0), 
            "minuto": IntVar(value = 0)
        }
        for indice, nome in enumerate(self.titulos):
            Label(self, text = nome).grid(row = indice)
            Entry(self, textvariable = self.titulos[nome]).grid(row = indice, column = 1)
        botao = Button(self, text = "Gerar licença", command = self.gerar)
        if self.atual >= self.total or self.pirateado:
            botao.config(state = DISABLED)
        botao.grid(row = 10, columnspan = 2)

    def gerar(self):
        '''
        Pega o valor dos widgets e passa para o criar_licenca
        '''
        if self.atual < self.total:
            dia = str(self.titulos['dia'].get())
            mes = str(self.titulos['mês'].get())
            ano = self.titulos['ano'].get()
            hora = self.titulos['hora'].get()
            minuto = self.titulos['minuto'].get()
            self.criar_licenca(dia, mes, ano, hora, minuto)
        else:
            messagebox.showwarning("Licença", 
        "Você atingiu o máximo de linceças geradas. Compre mais licenças.")

    def criar_licenca(self, dia, mes, ano, hora, minuto): 
        '''
        Criptografa uma mensagem com todos os dados (email e data)
        E escreve em um arquivo.
        '''
        f = Fernet(KEY)
        with open("licenca.key", "wb") as file:
            message = f"{dia}/{mes}/{ano}|{hora}:{minuto}"
            result = f.encrypt(message.encode())
            file.write(result)
        messagebox.showinfo("Informação", "Arquivo gerado.")
        self.atual += 1
        self.garantir_integridade()

    def garantir_integridade(self):
        '''
        Escreve na licença atual o número de licenças geradas
        Escreve no arquivo de integridade uma cópia disso.
        '''
        with open('license', 'wb') as file:
            message = f"{self.timestamp}|{self.atual}|{self.total}"
            result = f.encrypt(message.encode())
            file.write(result)
        with open(self.caminho, "r") as file:
            licencas = json.load(file)
            licencas[self.timestamp] = self.atual
        with open(self.caminho, "w") as file:
            json.dump(licencas, file)

path.expanduser('~user')
if __name__ == "__main__":
    key = KEY
    f = Fernet(key)
    try:
        with open("license", 'rb') as file:
            message = f.decrypt(file.readline())
            message = message.decode()
            timestamp, atual, total = message.split("|")
    except Exception as e:
        print(e)
        timestamp, atual, total = 0, 0, 0
    
    janela = Tk()
    janela.title("Licenciador")
    try:
        janela.iconbitmap("./assets/icone.ico")
    except:
        print("Não consegui encontrar o ícone")
    janela.geometry("+600+200")
    program = Gerador(janela, timestamp, int(atual), int(total))
    program.mainloop()