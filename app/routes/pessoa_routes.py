from flask import Blueprint, request, jsonify
from app.database import db, Pessoa

pessoa_bp = Blueprint("pessoa_bp", __name__)


@pessoa_bp.route("/", methods=["GET"])
def listar_pessoas():

    pessoas = Pessoa.query.all()

    lista = []

    for pessoa in pessoas:
        lista.append({
            "id": pessoa.id,
            "nome_completo": pessoa.nome_completo,
            "cpf": pessoa.cpf,
            "data_nascimento": pessoa.data_nascimento,
            "sexo": pessoa.sexo,
            "estado_civil": pessoa.estado_civil,
            "nacionalidade": pessoa.nacionalidade
        })

    return jsonify(lista)


@pessoa_bp.route("/criar", methods=["GET"])
def criar_pessoa_teste():

    pessoa = Pessoa(
        nome_completo="João Silva",
        cpf="123.456.789-00",
        data_nascimento="01/01/2000",
        sexo="Masculino",
        estado_civil="Solteiro",
        nacionalidade="Brasileiro"
    )

    db.session.add(pessoa)
    db.session.commit()

    return jsonify({
        "message": "Pessoa criada com sucesso"
    })