from flask import Flask, render_template, request
import sqlite3


app = Flask(__name__)

def banco_dados():   
    dados = sqlite3.connect('testando.db')
    cursor = dados.cursor()

    cursor.execute('SELECT * FROM cadeiras')
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
            return render_template("professor.html")
        elif nome == "aluno":
            #request.form["aluno"]
            return render_template("aluno.html")
    return render_template("index.html")

@app.route("/professor", methods = ["GET","POST"])
def professor():
   
    return render_template("professor.html")
        
@app.route("/aluno")
def aluno():
    return render_template("aluno.html")



@app.route('/cadeirasprofessor')
def cadeiras():
    dados_tabela, colunas_tabela = banco_dados()
    return render_template("cadeirasprofessor.html", dados_tabela = dados_tabela, colunas_tabela = colunas_tabela)

@app.route('/frequencia')
def frequencia():
    return render_template("frequencia.html")



if __name__ == "__main__":
    app.run(debug=True)

