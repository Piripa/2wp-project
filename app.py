from flask import Flask, render_template, request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pandas as pd
from datetime import date
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudantes.db'

db = SQLAlchemy(app)

class Estudante(db.Model):
    id = db.Column('id',db.Integer,primary_key = True,autoincrement = True)
    nome = db.Column(db.String(150))
    senha = db.Column(db.String(150))

    def __init__(self,nome,senha):
        self.nome = nome
        self.senha = senha

#variável global##################
tabela = 'Algoritmo'
##################################
def data():
    data_atual = date.today()
    dataTexto = data_atual.strftime('%d_%m_%Y')
    return dataTexto

def obter_dados(banco):
    dados = sqlite3.connect(banco)
    cursor = dados.cursor()
    cursor.execute("SELECT * FROM cadeiras")
    dados_tabela = cursor.fetchall()

    cursor.execute('PRAGMA table_info(cadeiras)')
    colunas_tabela = [col[1] for col in cursor.fetchall()]

    dados.close()

    return dados_tabela, colunas_tabela

@app.route("/" , methods = ["GET","POST"])
def home():

    if request.method == "POST":
        nome = request.form.get("nome")
        senha = request.form.get("senha")
        if nome == "professor":
            #request.form["professor"]
            return redirect("/professor")
        elif nome == "aluno":
            #request.form["aluno"]
            return redirect("/aluno")
    return render_template("index.html")

@app.route("/professor")
def professor():
    return render_template("professor.html")
        
@app.route("/aluno")
def aluno():
    return render_template("aluno.html")

@app.route("/cadeiras")
def cadeiras():
    dados_tabela, colunas_tabela = obter_dados('cadeiras.db')
    return render_template("cadeiras.html", dados_tabela = dados_tabela, colunas_tabela = colunas_tabela)

@app.route('/cadeirasprofessor')
def cadeirasprofessor():
    dados_tabela, colunas_tabela = obter_dados('testando.db')
    return render_template("cadeirasprofessor.html", dados_tabela = dados_tabela, colunas_tabela = colunas_tabela)

@app.route('/frequencia')
def frequencia():
    global tabela
    dados = sqlite3.connect('frequencia.db')
    cursor = dados.cursor()
    cursor.execute(f'SELECT * FROM {tabela}')
    frequencia = cursor.fetchall()
    dados.commit()
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    data = pd.read_sql(query,dados)
    list_table = []
    for coluna in data.columns:
        list_table = data[coluna].tolist()
    #retirando a tabela que é criada automaticamente pelo browser sqlite3
    list_table.remove('sqlite_sequence')
    cursor.close()
    dados.close()
    return render_template("frequencia.html", frequencia = frequencia, list_table = list_table, tabela = tabela) 

@app.route('/register')
def register():
    db.create_all()
    estudantes = Estudante.query.all()
    return render_template("register.html", estudantes = estudantes)

@app.route('/add', methods = ["GET","POST"])
def add():
    if request.method== "POST":
        estudante = Estudante(request.form['nome'],request.form['senha'])
        db.session.add(estudante)
        db.session.commit()
        return redirect(url_for('register'))
    return render_template("add.html")


@app.route('/edit/<int:id>', methods = ["GET", "POST"])
def edit(id):
    estudante = Estudante.query.get(id)
    if request.method == "POST":
        estudante.nome = request.form['nome']
        estudante.senha = request.form['senha']
        db.session.commit()
        return redirect(url_for('register'))
    return render_template("edit.html", estudante = estudante)


@app.route('/delete/<int:id>', methods = ["GET", "POST"])
def delete(id):
    estudante =Estudante.query.get(id)
    db.session.delete(estudante)
    db.session.commit()

    return redirect(url_for('register'))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/cadastrarCadeira',methods = ['POST'])
def cadastrarFrequencia():
    global tabela
    dados = sqlite3.connect('frequencia.db')
    cursor = dados.cursor()
    frequencia = request.form.get('cadeira')
    tabela = frequencia
    nome = request.form.get('nome')
    matricula = request.form.get('matricula')
    horario = request.form.get('horario')
    verificar = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{frequencia}'"
    cursor.execute(verificar)
    resultado = cursor.fetchone()  
    if resultado:
        cursor.execute('INSERT INTO {} VALUES ("{}","{}","{}");'.format(frequencia,nome,matricula,horario))
        print("Cadastrado aluno em uma tabela existente")
    else:
        cursor.execute('CREATE TABLE {} (nome TEXT NOT NULL,matricula TEXT NOT NULL,horario time);'.format(frequencia))
        cursor.execute('INSERT INTO {} VALUES ("{}","{}","{}");'.format(frequencia,nome,matricula,horario))
        print("Cadastrado aluno em uma tabela nova")
    dados.commit()
    cursor.close()
    dados.close()
    return redirect('/frequencia')

@app.route("/excluirFrequencia", methods = ['POST'])
def excluirFrequencia():
    global tabela
    dados = sqlite3.connect('frequencia.db')
    cursor = dados.cursor()
    dadoId = request.form.get('dado')
    cursor.execute(f"DELETE FROM {tabela} WHERE nome= '{dadoId}';")
    dados.commit()
    cursor.close()
    dados.close()
    return redirect('/frequencia')  

@app.route("/paginaCadCadeiras", methods= ['POST'])
def paginaCadCadeiras():
   return render_template("cadastrarCadeira.html")

@app.route("/irPageCadFreq", methods =['POST'])
def irPageCadFreq():
    return redirect('/frequencia')

@app.route("/paginaCadFreq")
def paginaCadFreq():
   global tabela
   dados = sqlite3.connect('frequencia.db')
   cursor = dados.cursor()
   cursor.execute(f"SELECT * FROM {tabela};")
   alunos = cursor.fetchall()
   dados.commit()
   #-------------------Abaixo: Lendo nomes das tabelas-------------------
   query = "SELECT name FROM sqlite_master WHERE type='table';"
   data = pd.read_sql(query,dados)
   list_table = []
   for coluna in data.columns:
       list_table = data[coluna].tolist()
   list_table.remove('sqlite_sequence')
   cursor.close()
   dados.close
   return render_template("cadastroFrequencia.html", list_table = list_table, alunos = alunos)

@app.route("/selecionarTabela", methods = ['POST'])
def selecionarTabela():
    global tabela
    pesquisar = request.form.get('nome')
    tabela = pesquisar
    return redirect('/frequencia')

@app.route("/combobox", methods = ['GET','POST'])
def combobox():
    global tabela
    pesquisar = request.form.get('acessoTabela')
    tabela = pesquisar
    return redirect('/paginaCadFreq')

@app.route("/presenca", methods = ['GET','POST'])
def presenca():
    global tabela
    if request.method== "POST":
        list_presenca_comp = request.form.getlist('presente')
        auxiliar = ''
        list_presenca = []
        for i in list_presenca_comp:
            auxiliar = i
            list_presenca.append(auxiliar.split())
        print(list_presenca)
        dados = sqlite3.connect('presenca.db')
        cursor = dados.cursor()
        tabela_for_frequencia = tabela+"_"+data()
        cursor.execute('CREATE TABLE IF NOT EXISTS {} (nome TEXT NOT NULL, matricula TEXT NOT NULL, presenca TEXT);'.format(tabela_for_frequencia))
        for i in list_presenca:
            nome = i[0]
            matricula = i[1]
            estar_presente = i[3]
            cursor.execute(f"INSERT INTO {tabela_for_frequencia} VALUES ('{nome}','{matricula}','{estar_presente}')")
        dados.commit()
        cursor.close()
        dados.close()
    return redirect('/paginaCadFreq')










if __name__ in '__name__':
    app.run(debug=True)

