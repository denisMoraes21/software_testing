import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', 'app.db')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()

    conn.execute('''CREATE TABLE IF NOT EXISTS candidatos
                    (
                        id
                        INTEGER
                        PRIMARY
                        KEY
                        AUTOINCREMENT,
                        numero
                        TEXT
                        NOT
                        NULL,
                        nome
                        TEXT
                        NOT
                        NULL,
                        partido
                        TEXT
                        NOT
                        NULL,
                        cargo
                        TEXT
                        NOT
                        NULL,
                        foto
                        TEXT
                    )''')

    conn.execute('''CREATE TABLE IF NOT EXISTS votos
                    (
                        id
                        INTEGER
                        PRIMARY
                        KEY
                        AUTOINCREMENT,
                        cargo
                        TEXT
                        NOT
                        NULL,
                        numero_candidato
                        TEXT,
                        tipo_voto
                        TEXT
                        NOT
                        NULL,
                        data_hora
                        TIMESTAMP
                        DEFAULT
                        CURRENT_TIMESTAMP
                    )''')

    # Mock de dados com 2 dígitos para facilitar o teste
    if conn.execute('SELECT COUNT(*) FROM candidatos').fetchone()[0] == 0:
        candidatos = [
            # Candidatos a Prefeito
            ('12', 'João Silva', 'Partido A', 'Prefeito', 'https://via.placeholder.com/100/0000FF'),
            ('34', 'Maria Souza', 'Partido B', 'Prefeito', 'https://via.placeholder.com/100/FF0000'),
           

            # Candidatos a Governador
            ('56', 'Carlos Mendes', 'Partido C', 'Governador', 'https://via.placeholder.com/100/00FF00'),
            ('78', 'Ana Dias', 'Partido D', 'Governador', 'https://via.placeholder.com/100/FFFF00'),

            # Candidatos a Presidente
            ('90', 'Pedro Paulo', 'Partido E', 'Presidente', 'https://via.placeholder.com/100/FF00FF'),
            ('88', 'Lucas Fernandes', 'Partido G', 'Presidente', 'https://via.placeholder.com/100/111111')
        ]
        conn.executemany("INSERT INTO candidatos (numero, nome, partido, cargo, foto) VALUES (?, ?, ?, ?, ?)",
                         candidatos)

    conn.commit()
    conn.close()