#importa bibliotecas
from flask import Flask, request, redirect, session, jsonify
from flask_cors import CORS
import bcrypt, json, sqlite3, os
from datetime import datetime, timedelta

#iniciando o flask
app = Flask(__name__)
app.secret_key = os.urandom(24)
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

    if not usuario_id:
        return jsonify({"erro": "não autorizado"}), 401

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

#mostra dados para gráfico
@app.route('/mostra-dados')
def mostra_dados():
    usuario_id = session.get('user_id', -1)
    if not usuario_id:
        return jsonify({"erro": "não autorizado"}), 401
    
    conn = sqlite3.connect('pystudy.db')
    cur = conn.cursor()

    cur.execute('SELECT materia, dia, tempo, acert, feitas FROM dados WHERE usuario_id = ? AND dia >= date(\'now\', \'-7 days\') ORDER BY dia ASC', (usuario_id,))

    dados = cur.fetchall()
    conn.close()

    hoje = datetime.now()
    dias = [(hoje - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]

    dados_t = {}
    for x in dados:
        materia = x[0]

        if materia not in dados_t:
            dados_t[materia] = []

        dados_t[materia].append({
            "dia": x[1],
            "tempo": x[2],
            "acertos": x[3],
            "feitas": x[4]
        })

    for materia in dados_t:
        dias_db = [d["dia"] for d in dados_t[materia]]
        for dia in dias:
            if dia not in dias_db:
                dados_t[materia].append({
                "dia": dia,
                "tempo": 0,
                "acertos": 0,
                "feitas": 0
            })
        
        dados_t[materia].sort(key=lambda x: x["dia"])

    return jsonify(dados_t)

#roda o flask
app.run(debug=True)