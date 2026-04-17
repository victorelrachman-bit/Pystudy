#importa bibliotecas
import sqlite3
from flask import Flask, request, redirect, session
from flask_cors import CORS

#iniciando o flask
app = Flask(__name__)
app.secret_key = "123"
CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5500"])

#iniciando banco de dados
def init_db():
    conn = sqlite3.connect('pystudy.db')
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            senha TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

#verifica se esta logado
@app.route('/status')
def status():
    return {"logado": session.get("logado", False)}

#faz login
@app.route('/login', methods=['POST'])
def recebe_dados():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    conn = sqlite3.connect('pystudy.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM usuarios WHERE nome=? AND senha=?", (nome, senha))
    user = cur.fetchone()
    conn.close()

    if user:
        session['logado'] = True
        return redirect('http://127.0.0.1:5500/graficos.html')
    else:
        session['logado'] = False
        return redirect('http://127.0.0.1:5500/index.html')


   

#faz cadastro
@app.route('/cadastro', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    conn = sqlite3.connect('pystudy.db')
    cur = conn.cursor()

    cur.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, senha))

    conn.commit()
    conn.close()

    return redirect('http://127.0.0.1:5500/index.html')

#roda o flask
app.run(debug=True)