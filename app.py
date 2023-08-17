from flask import Flask, render_template, request,redirect,flash,url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, login_user
from func.funcoes import criptografar_senha, comparar_senhas
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SECRET_KEY'] = 'twowp'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_username):
    return Usuarios.get(user_username).first()
 


class Usuarios(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    password = db.Column(db.String(80), nullable = False)
  


    def __init__(self,username,password):
        self.username = username
        self.password = password


class RegisterForm(FlaskForm):
    username =  StringField(validators=[InputRequired(), Length(
    min=4,max=20)], render_kw={"placeholder":"Username"})

    password =  PasswordField(validators=[InputRequired(), Length(
    min=4,max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Register")

    def validar_usuario(self,username):
        usuario_existente = Usuarios.query.filter_by(username=username).first()
        if usuario_existente:
            raise ValidationError("Esse usuário já existe. Escolha outro diferente")
   

class LoginForm(FlaskForm):
    username =  StringField(validators=[InputRequired(), Length(
    min=4,max=20)], render_kw={"placeholder":"Username"})

    password =  PasswordField(validators=[InputRequired(), Length(
    min=4,max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Login")


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
    form = LoginForm() 
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(username=form.username.data).first()
        print(user)
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else: 
            print("Usuário não encontrado!")
    return render_template("/index.html", form = form)


@app.route("/dashboard", methods = ["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

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


@app.route('/register', methods = ["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        novo_user = Usuarios(username=form.username.data,password=hashed_password)
        db.session.add(novo_user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html", form = form)



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
    db.create_all()
    app.run(debug=True)

