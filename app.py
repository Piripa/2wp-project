from flask import Flask, render_template, request,redirect,flash,session
import sqlite3
import pandas as pd
from datetime import date
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.secret_key = 'ola'


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
        username = request.form.get('username')
        password = request.form.get('password')
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        c.execute("SELECT * FROM login WHERE username = ?" , (username,))
        data = c.fetchone()
        conn.close()
        if data:
            stored_password = data[1]
            user = data[2]

            if sha256_crypt.verify(password,stored_password):
                if user =='Professor':
                    return render_template("/professor.html")
                elif user == 'Aluno':
                    return render_template("/aluno.html")
            else: 
                flash("USUÁRIO OU SENHA INCORRETOS")
                return render_template("/index.html")
    return render_template("/index.html")


@app.route("/professor", methods = ["GET","POST"])
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

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = sha256_crypt.hash(request.form.get('password'))
        user = request.form.get('user')
        conn = sqlite3.connect('login.db')
        c = conn.cursor()

        #Procura se existe algum usuário já cadastrado no BD
        c.execute("SELECT * FROM login WHERE username = ?", (username,))
        existing_user = c.fetchone()
        if existing_user:
            conn.close()
            flash("Usuário já existente", "error")
            return render_template("register.html")
        
        #Caso não exista, ele adiciona
        c.execute("INSERT INTO login (username, password, user) VALUES (?, ?, ?)", (username, password, user))
        conn.commit()
        conn.close()
        flash("Cadastro Realizado com Sucesso", "success")
        
    return render_template("register.html")


@app.route('/cadastrarCadeira',methods = ['POST'])
def cadastrarFrequencia():
    global tabela
    dados = sqlite3.connect('frequencia.db')
    cursor = dados.cursor()
    frequencia = request.form.get('acessoTabela')
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
    return render_template("cadastrarCadeira.html", list_table=list_table)

# @app.route("/irPageCadFreq", methods =['POST'])
# def irPageCadFreq():
#     return redirect('/frequencia')

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
    return redirect('/frequencia')

if __name__ in '__name__':
    app.run(debug=True)
