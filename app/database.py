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

    # 1. Tabela de Eleitores (AGORA COM A COLUNA ja_votou)
    conn.execute('''CREATE TABLE IF NOT EXISTS eleitores
                    (
                        id
                        INTEGER
                        PRIMARY
                        KEY
                        AUTOINCREMENT,
                        nome
                        TEXT
                        NOT
                        NULL
                        UNIQUE,
                        ja_votou
                        INTEGER
                        DEFAULT
                        0
                    )''')

    # 2. Tabela de Candidatos
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

    # 3. Tabela de Votos
    conn.execute('''CREATE TABLE IF NOT EXISTS votos
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        eleitor_id
        INTEGER,
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
        CURRENT_TIMESTAMP,
        FOREIGN
        KEY
                    (
        eleitor_id
                    ) REFERENCES eleitores
                    (
                        id
                    ))''')

    # Insere os dados de teste se estiver vazio
    if conn.execute('SELECT COUNT(*) FROM candidatos').fetchone()[0] == 0:
        # Mock de Eleitores
        conn.executemany("INSERT INTO eleitores (nome) VALUES (?)", [('Adeilso',), ('Denis',)])

        # Mock de Candidatos
        candidatos = [
            ('12', 'João Silva', 'Partido A', 'Prefeito', 'https://via.placeholder.com/100/0000FF'),
            ('34', 'Maria Souza', 'Partido B', 'Prefeito', 'https://via.placeholder.com/100/FF0000'),
            ('56', 'Carlos Mendes', 'Partido C', 'Governador', 'https://via.placeholder.com/100/00FF00'),
            ('78', 'Ana Dias', 'Partido D', 'Governador', 'https://via.placeholder.com/100/FFFF00'),
            ('90', 'Pedro Paulo', 'Partido E', 'Presidente', 'https://via.placeholder.com/100/FF00FF')
        ]
        conn.executemany("INSERT INTO candidatos (numero, nome, partido, cargo, foto) VALUES (?, ?, ?, ?, ?)",
                         candidatos)

    conn.commit()
    conn.close()