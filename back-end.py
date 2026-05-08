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
    

