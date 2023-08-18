from flask import Flask, render_template, request,redirect,flash,url_for
import sqlite3
from flask_login import LoginManager, UserMixin, login_required, login_user
from passlib.hash import sha256_crypt





app = Flask(__name__)
# def create_table():
#     conn = sqlite3.connect('login.db')
#     c = conn.cursor()
#     c.execute("CREATE TABLE IF NOT EXISTS login (username TEXT, password TEXT)")
#     conn.commit()
#     conn.close()

# create_table()


#variável global
tabela = 'Algoritmo'

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
        print(password)
        print(username)
        data = c.fetchone()
        conn.close()
        if data:
            if sha256_crypt.verify(password,data[1]):
                return render_template("/professor.html")
            
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
    cursor.close()
    dados.close()
    return render_template("frequencia.html", frequencia = frequencia, tabela = tabela) 


@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = sha256_crypt.hash(request.form.get('password'))
        conn = sqlite3.connect('login.db')
        c = conn.cursor()
        c.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
    return render_template("register.html")


@app.route('/cadastrarFrequencia',methods = ['POST'])
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

@app.route("/readFrequencia", methods = ['POST'])
def readFrequencia():
    global tabela
    read = request.form.get('tabelaFre')
    dados = sqlite3.connect('frequencia.db')
    cursor = dados.cursor()
    verificar = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{read}'"
    cursor.execute(verificar)
    resultado = cursor.fetchone()
    if  resultado:
        tabela = read
        redirect('/frequencia')
    return redirect('/frequencia')

if __name__ in '__name__':
    app.run(debug=True)