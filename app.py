from flask import Flask, render_template, request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

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
            return render_template("professor.html")
        elif nome == "aluno":
            return render_template("aluno.html")
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
    return render_template("frequencia.html")

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

if __name__ =="__main__":
    
    app.run(debug=True)




