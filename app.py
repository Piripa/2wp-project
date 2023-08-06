from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

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
    cursor.close()
    dados.close()
    return render_template("frequencia.html", frequencia = frequencia, tabela = tabela) 

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

