#importa bibliotecas
import sqlite3
from flask import Flask, request, redirect, session
from flask_cors import CORS
import bcrypt

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

def init_db_dados():
    conn = sqlite3.connect('pystudy.db')
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS dados (id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                materia TEXT,
                dia DATE,
                tempo INTEGER,
                acert INTEGER,
                feitas INTEGER,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id))
    """)

    conn.commit()
    conn.close()

init_db()
init_db_dados()

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

    cur.execute("SELECT * FROM usuarios WHERE nome=?", (nome,))
    user = cur.fetchone()
    conn.close()

    if user:
        hash_salvo = user[2]
        hash_salvo = hash_salvo.encode('utf-8')

        if bcrypt.checkpw(senha.encode('utf-8'), hash_salvo):
            session['logado'] = True
            session['user_id'] = user[0]

            return redirect('http://127.0.0.1:5500/graficos.html')
        
    session['logado'] = False
    return redirect('http://127.0.0.1:5500/index.html')

#faz cadastro
@app.route('/cadastro', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    senha = request.form.get('senha')


    conn = sqlite3.connect('pystudy.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM usuarios WHERE nome=?', (nome,))
    user = cur.fetchone()

    if user:
        conn.close()
        return redirect('http://127.0.0.1:5500/cadastro.html?erro=usuario_existe')
    else:
        senha_bytes = senha.encode('utf-8')
        hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')

        cur.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, hash_senha))

        conn.commit()
        conn.close()

        return redirect('http://127.0.0.1:5500/index.html')

#envia dados de grafico pro banco
@app.route('/envio-de-dados', methods=['POST'])
def envio_de_dados():
    usuario_id = session.get('user_id')

    materia = request.form.get('materia')
    dia = request.form.get('dia')
    tempo = request.form.get('tempo')
    acertos = request.form.get('acert')
    feitas = request.form.get('feitas')

    conn = sqlite3.connect('pystudy.db')
    cur = conn.cursor()

    cur.execute("""INSERT INTO dados (usuario_id, materia, dia, tempo, acert, feitas) 
                VALUES (?, ?, ?, ?, ?, ?)""", 
                (usuario_id, materia, dia, tempo, acertos, feitas))

    conn.commit()
    conn.close()

    return redirect('http://127.0.0.1:5500/graficos.html')


#roda o flask
app.run(debug=True)