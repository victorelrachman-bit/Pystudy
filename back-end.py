#importa bibliotecas
from flask import Flask, request, redirect, session, jsonify
from flask_cors import CORS
import bcrypt, json, sqlite3, os
from datetime import datetime, timedelta

class Database:
    def __init__(self, db_name):
        self.__db_name = db_name

    def connect(self):
        return sqlite3.connect(self.__db_name)
    
    def create(self):
        conn = self.connect()
        cur = conn.cursor()
        
        cur.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            senha TEXT
        )
        """)

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
    
    def execute(self, query, params=()):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        conn.close()
    
    def fetchall(self, query, params=()):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query, params)
        dados = cur.fetchall()
        conn.close()
        return dados
    
    def fetchone(self, query, params=()):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(query, params)
        dados = cur.fetchone()
        conn.close()
        return dados
    
class AuthService:
    def __init__(self, db):
        self.__db = db

    def register(self, nome, senha):
        user = self.__db.fetchone("SELECT * FROM usuarios WHERE nome=?", (nome,))

        if user:
            return False
        
        senha_bytes = senha.encode('utf-8')
        hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode('utf-8')
        self.__db.execute("INSERT INTO usuarios (nome, senha) VALUES (?, ?)", (nome, hash_senha))

    def login(self, nome, senha):
        user = self.__db.fetchone("SELECT * FROM usuarios WHERE nome=?", (nome,))

        if user:
            hash_salvo = user[2]
            hash_salvo = hash_salvo.encode('utf-8')

            if bcrypt.checkpw(senha.encode('utf-8'), hash_salvo):
                return user
            
        return None
    
    