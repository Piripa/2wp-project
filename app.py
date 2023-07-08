from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/professor")
def professor():
    return render_template("professor.html")

@app.route("/aluno")
def aluno():
    return render_template("aluno.html")

