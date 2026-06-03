from flask import Blueprint, jsonify, request
from app.database import get_db_connection

urna_bp = Blueprint('urna', __name__)

@urna_bp.route('/api/candidatos', methods=['GET'])
def get_candidatos():
    cargo = request.args.get('cargo')
    conn = get_db_connection()
    candidatos = conn.execute('SELECT * FROM candidatos WHERE cargo = ?', (cargo,)).fetchall()
    conn.close()
    return jsonify([dict(c) for c in candidatos])

@urna_bp.route('/api/candidato', methods=['GET'])
def get_candidato():
    numero = request.args.get('numero')
    cargo = request.args.get('cargo')
    conn = get_db_connection()
    candidato = conn.execute('SELECT * FROM candidatos WHERE numero = ? AND cargo = ?', (numero, cargo)).fetchone()
    conn.close()
    return jsonify(dict(candidato)) if candidato else jsonify({'error': 'Nao encontrado'}), 404

@urna_bp.route('/api/votar', methods=['POST'])
def registrar_voto():
    dados = request.json
    conn = get_db_connection()
    conn.execute('INSERT INTO votos (cargo, numero_candidato, tipo_voto) VALUES (?, ?, ?)',
                 (dados.get('cargo'), dados.get('numero'), dados.get('tipo')))
    conn.commit()
    conn.close()
    return jsonify({'status': 'sucesso'})

@urna_bp.route('/api/relatorio', methods=['GET'])
def gerar_relatorio():
    conn = get_db_connection()
    # Junta os votos com os candidatos para pegar o nome
    query = '''
        SELECT v.cargo, v.tipo_voto, v.numero_candidato, c.nome, COUNT(v.id) as total_votos
        FROM votos v
        LEFT JOIN candidatos c ON v.numero_candidato = c.numero AND v.cargo = c.cargo
        GROUP BY v.cargo, v.tipo_voto, v.numero_candidato, c.nome
        ORDER BY v.cargo, total_votos DESC
    '''
    relatorio = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(r) for r in relatorio])