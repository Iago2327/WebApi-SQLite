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
                
            id INTEGER NOT NULL PRIMARY KEY autoincrement,
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
    def __init__(self, ra, nome, email, media):
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
        sql = 'INSERT INTO Alunos(ra, nome, email, media) values(?, ?, ?, ?)'
        #Ler e executar comando de sql puro no bd
        bd.execute(sql,(aluno.ra, aluno.nome, aluno.email, aluno.media,))

        conn.commit()

        return{'success': 'Aluno inserido com sucesso!'}, 200
    except Exception as erro:
        return{'erro':erro}

@Server.route('/home/apagar/<int:id>', methods = ['DELETE'])
def deleta_aluno(id):
    try:
        sql = 'DELETE * FROM Alunos WHERE id=(?)'
        bd.execute(sql, (id))
        conn.commit()
        return {'success': 'Aluno deletado com sucesso!'}, 200
    except Exception as erro:
        return {'erro': erro}, 500

@Server.route('/home/listar')
def Listar_Aluno():
    try:
        sql = 'SELECT * FROM Alunos'
        alunos = bd.execute(sql).fetchall()
        print(alunos)
        return {"success":alunos}
    except Exception as erro:
        return{'erro':erro}, 500

@Server.route('/home/filtro/<int:id>', methods = ["GET"])
def Filtrar_Aluno(id):
    try:
        sql = 'SELECT * FROM Alunos WHERE id=?'
        alunos = bd.execute(sql, (id)).fetchall()
        return {"success": alunos}
    except Exception as erro:
        return {'erro':erro}, 500
    
@Server.route('/home/update/<int:id>', methods = ["PUT"])
def Atualizar_Alunos():
    try:
        data = request.get_json()
        sql = 'UPDATE Alunos SET nome=?, email=?, media=? WHERE id=?'
        bd.execute(sql, (data['nome'], data['email'], data['media'], id))
        conn.commit()
        return {'success':'Aluno atualizado com sucesso!'}, 200
    except Exception as erro:
        return{'erro':erro}, 500

if __name__ == "__main__":
    Server.run(debug=True, port=1800)

