import json
import requests as rq

url = 'http://localhost:1800/'

def inserir():
    ra = str(input('RA do Aluno: '))
    nome = str(input('Nome do Aluno: '))
    email = str(input('EMAIL do Aluno: '))
    media = str(input('Media do Aluno: '))
    data = {
        "nome" : nome,
        "email" : email,
        "media" : media
    }
    req = rq.post(url + '/home/inserir', data = json.dumps(data))
    if req.status_code == 200:
        print("Dados inseridos com sucesso!")
        print(req.json())
    else:
        print("Falha ao inserir dados.")
        print(req.text)

def apagar():
    id = int(input('Digite o ID do aluno: '))
    req = rq.delete(url + '/home/apagar', json = id).json()
    datas = req['success']
    if len(datas) == 0:
        print(req)
    else:
        print(datas)

def listar():
    req = rq.get(url + 'home/listar')
    print(req.content)

def filtro():
    id = int(input('Digite o ID do aluno: '))
    req = rq.get(url + 'home/filtro', json = id).json()
    datas = req['success']
    if len(datas) == 0:
        print(req)
    else:
        print(datas)

def update():
    id = int(input('Digite o ID do aluno: '))
    nome = str(input('NOVO Nome do Aluno: '))
    email = str(input('NOVO EMAIL do Aluno: '))
    media = str(input('NOVO Media do Aluno: '))
    data = {
        "id" : id,
        "nome" : nome,
        "email" : email,
        "media" : media
    }
    req = rq.post(url + 'home/update', json = data).json()
    datas = req['success']
    if len(datas) == 0:
        print(req)
    else:
        print(datas)

def menu():
    print("***************** MENU *****************")
    print("1) Inserir Aluno")
    print("2) Deletar Aluno")
    print("3) Atualizar Aluno")
    print("4) Listar TODOS os Alunos")
    print("5) Filtrar por Alunos")
    print("6) Sair")
    print("***************** MENU *****************")

req = rq.get(url + 'home').json()
print(req)
while True:
    menu()
    op = int(input("\n Digite a opcao desejada:\n"))
    if op == 1:
        inserir()
    elif op == 2:
        apagar()
    elif op == 3:
        update()
    elif op == 4:
        listar()
    elif op == 5:
        filtro()
    elif op == 6:
        print("Saindo.........")
        break
    else:
        print("Opcao invalida")