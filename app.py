from flask import Flask, render_template, request
app = Flask(__name__)

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

@app.route("/professor")
def professor():
    return render_template("professor.html")
        
@app.route("/aluno")
def aluno():
    return render_template("aluno.html")

