#importa bibliotecas
from flask import Flask, request, redirect, session, jsonify
from flask_cors import CORS
import os
from model import Database, AuthService, StudyService

#inicia o flask
app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

#inicia o banco
db = Database("pystudy.db")
db.create()

#servicos
auth = AuthService(db)
study = StudyService(db)

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    user = auth.cadastro(nome, senha)
    if user == None:
        return redirect('http://127.0.0.1:5500/cadastro.html?erro=usuario_existe')

    if user:
        session['logado'] = True
        session['user_id'] = user[0]

        return redirect('http://127.0.0.1:5500/graficos.html')

    return redirect('http://127.0.0.1:5500/cadastro.html')

@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    user = auth.login(nome, senha)

    if user:
        session['logado'] = True
        session['user_id'] = user[0]

        return redirect('http://127.0.0.1:5500/graficos.html')

    session['logado'] = False
    session.pop('user_id', None)

    return redirect('http://127.0.0.1:5500/index.html')

@app.route('/status')
def status():
    return {"logado": session.get("logado", False)}

@app.route('/envio-de-dados', methods=['POST'])
def envio():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"erro": "não autorizado"}), 401
    
    study.addData(user_id, 
        request.form.get('materia'),
        request.form.get('dia'),
        request.form.get('tempo'),
        request.form.get('acert'),
        request.form.get('feitas'))
    
    return redirect('http://127.0.0.1:5500/graficos.html')

@app.route('/mostra-dados')
def mostra():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"erro": "não autorizado"}), 401
    
    return jsonify(study.get_last_week(user_id))

@app.route('/logoff')
def logoff():
    session.pop('user_id', None)
    session['logado'] = False

    return redirect('http://127.0.0.1:5500/index.html')

#inicia o app
app.run(debug=True)