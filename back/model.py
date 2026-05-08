#importa bibliotecas
import bcrypt
import sqlite3
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
        CREATE TABLE IF NOT EXISTS dados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            materia TEXT,
            dia DATE,
            tempo INTEGER,
            acert INTEGER,
            feitas INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
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

    def cadastro(self, nome, senha):

        user = self.__db.fetchone(
            "SELECT * FROM usuarios WHERE nome=?",
            (nome,)
        )

        if user:
            return None

        senha_bytes = senha.encode('utf-8')

        hash_senha = bcrypt.hashpw(
            senha_bytes,
            bcrypt.gensalt()
        ).decode('utf-8')

        self.__db.execute(
            "INSERT INTO usuarios (nome, senha) VALUES (?, ?)",
            (nome, hash_senha)
        )

        user = self.__db.fetchone(
            "SELECT * FROM usuarios WHERE nome=?", (nome,))

        return user

    def login(self, nome, senha):

        user = self.__db.fetchone(
            "SELECT * FROM usuarios WHERE nome=?",
            (nome,)
        )

        if user:

            hash_salvo = user[2].encode('utf-8')

            if bcrypt.checkpw(
                senha.encode('utf-8'),
                hash_salvo
            ):
                return user

        return None


class StudyService:

    def __init__(self, db):
        self.__db = db

    def addData(
        self,
        user_id,
        materia,
        dia,
        tempo,
        acertos,
        feitas
    ):

        self.__db.execute("""
            INSERT INTO dados (
                usuario_id,
                materia,
                dia,
                tempo,
                acert,
                feitas
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            materia,
            dia,
            tempo,
            acertos,
            feitas
        ))

    def get_last_week(self, user_id):

        dados = self.__db.fetchall("""
            SELECT
                materia,
                dia,
                tempo,
                acert,
                feitas
            FROM dados
            WHERE usuario_id = ?
            AND dia >= date('now', '-7 days')
            ORDER BY dia ASC
        """, (user_id,))

        hoje = datetime.now()

        dias = [
            (hoje - timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(6, -1, -1)
        ]

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

            dias_db = [
                d["dia"]
                for d in dados_t[materia]
            ]

            for dia in dias:

                if dia not in dias_db:

                    dados_t[materia].append({
                        "dia": dia,
                        "tempo": 0,
                        "acertos": 0,
                        "feitas": 0
                    })

            dados_t[materia].sort(
                key=lambda x: x["dia"]
            )

        return dados_t