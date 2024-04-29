from flask import Flask, request
import sqlite3
from sqlite3 import Error

#conectando ao bd
conn = sqlite3.connect('primeiro.db', check_same_thread=False)

#Definindo cursor(função que permite a navegação e manipulação dos registro do bd)
cursor = conn.cursor()

#criando tabela "o bd" (execute: função que lê e executa comando de SQL puro diretamento no bd)
def bd():
    bd.execute("""
                
    CREATE TABLE if not exists Alunos(
                
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            ra TEXT NOT NULL,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            media INTEGER NOT NULL
    );
    """)
    conn.commit()
    print("Tabela criada com sucesso!")

#Criando classe para facilitar na manipulação de informação entre servidor e bd
class Aluno:
    def __init__(self, id, ra, nome, email, media):
        self.id = id
        self.ra = ra
        self.nome = nome
        self.email = email
        self.media = media

Server = Flask(__name__)

#pagina para verificar conexão apenas
@Server.route('/home', methods = ['GET'])
def home():
    return {"connected": "Conexeção bem sucessida!"}

#inserido um novo aluno
@Server.route('/home/inserir', methods = ['POST'])
def insere_aluno():
    try:
        #recebe dados do cliente
        data = request.get_json()
        #cria um objeto na classe aluno(um novo aluno e suas respequitivas informações)
        aluno = Aluno(data['ra'], data['nome'], data['email'], data['media'])
        #Inserido as informações do novo objeto no bd
        sql = 'insert into Alunos(ra, nome, email, media) values(?, ?, ?, ?)'
        #Ler e executar comando de sql puro no bd
        bd.execute(sql,(aluno.ra, aluno.nome, aluno.email, aluno.media,))

        conn.commit()

        return{'success': 'Aluno inserido com sucesso!'}, 200
    except Exception as erro:
        return{'erro':erro}

@Server.route('/home/Delete/<int=id>', methods = ['DELETE'])
def deleta_aluno(id):
    try:
        sql = 'delete from Alunos where id=(?)'
        bd.execute(sql, (id))
        conn.commit()
        return {'success': 'Aluno deletado com sucesso!'}, 200
    except Exception as erro:
        return {'erro': erro}, 500

#desconectar do db
conn.close()

