from flask import Blueprint, jsonify, request
from app.database import get_db_connection

urna_bp = Blueprint('urna', __name__)


# --- ROTAS DE ELEITORES (CRUD) ---
@urna_bp.route('/api/eleitores', methods=['GET', 'POST'])
def gerenciar_eleitores():
    conn = get_db_connection()
    if request.method == 'POST':
        nome = request.json.get('nome')
        conn.execute('INSERT INTO eleitores (nome) VALUES (?)', (nome,))
        conn.commit()
        return jsonify({'status': 'sucesso'})
    else:
        eleitores = conn.execute('SELECT * FROM eleitores').fetchall()
        return jsonify([dict(e) for e in eleitores])


@urna_bp.route('/api/eleitores/<int:id>', methods=['PUT', 'DELETE'])
def alterar_eleitor(id):
    conn = get_db_connection()
    if request.method == 'PUT':
        nome = request.json.get('nome')
        conn.execute('UPDATE eleitores SET nome = ? WHERE id = ?', (nome, id))
    elif request.method == 'DELETE':
        conn.execute('DELETE FROM eleitores WHERE id = ?', (id,))
        conn.execute('DELETE FROM votos WHERE eleitor_id = ?', (id,))  # Apaga os votos do eleitor também
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})


@urna_bp.route('/api/eleitores/<int:id>/encerrar', methods=['POST'])
def encerrar_votacao_eleitor(id):
    conn = get_db_connection()
    # Marca o eleitor como "já votou" (1)
    conn.execute('UPDATE eleitores SET ja_votou = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

# --- ROTAS DA URNA ---
@urna_bp.route('/api/candidatos', methods=['GET'])
def get_candidatos():
    cargo = request.args.get('cargo')
    conn = get_db_connection()
    candidatos = conn.execute('SELECT * FROM candidatos WHERE cargo = ?', (cargo,)).fetchall()
    conn.close()
    return jsonify([dict(c) for c in candidatos])


@urna_bp.route('/api/votar', methods=['POST'])
def registrar_voto():
    dados = request.json
    conn = get_db_connection()
    # Agora salva o ID do eleitor junto com o voto
    conn.execute('INSERT INTO votos (eleitor_id, cargo, numero_candidato, tipo_voto) VALUES (?, ?, ?, ?)',
                 (dados.get('eleitor_id'), dados.get('cargo'), dados.get('numero'), dados.get('tipo')))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})


@urna_bp.route('/api/relatorio', methods=['GET'])
def gerar_relatorio():
    eleitor_id = request.args.get('eleitor_id')
    conn = get_db_connection()

    if eleitor_id:  # Relatório específico de um eleitor
        query = '''
                SELECT v.cargo, v.tipo_voto, v.numero_candidato, c.nome
                FROM votos v
                         LEFT JOIN candidatos c ON v.numero_candidato = c.numero AND v.cargo = c.cargo
                WHERE v.eleitor_id = ? \
                '''
        relatorio = conn.execute(query, (eleitor_id,)).fetchall()
    else:  # Relatório geral de todos os votos
        query = '''
                SELECT v.cargo, v.tipo_voto, v.numero_candidato, c.nome, COUNT(v.id) as total_votos
                FROM votos v
                         LEFT JOIN candidatos c ON v.numero_candidato = c.numero AND v.cargo = c.cargo
                GROUP BY v.cargo, v.tipo_voto, v.numero_candidato, c.nome
                ORDER BY v.cargo, total_votos DESC \
                '''
        relatorio = conn.execute(query).fetchall()

    conn.close()
    return jsonify([dict(r) for r in relatorio])