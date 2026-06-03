from flask import Blueprint, request, render_template
from app.data.services.pessoas_services import PessoaService

pessoa_bp = Blueprint(
    "pessoas", __name__, template_folder="templates")


@pessoa_bp.route("/create", methods=["POST"])
def create_pessoa():
    print("Rota create_pessoa chamada")

    data = request.get_json()

    print(data)

    try:

        pessoa = PessoaService.create_pessoa(
            nome_completo=data["nome_completo"],
            cpf=data["cpf"],
            data_nascimento=data["data_nascimento"],
            sexo=data["sexo"],
            estado_civil=data["estado_civil"],
            nacionalidade=data["nacionalidade"],
            telefone=data["telefone"],
            celular=data["celular"],
            email=data["email"],
            cep=data["cep"],
            logradouro=data["logradouro"],
            numero=data["numero"],
            complemento=data["complemento"],
            bairro=data["bairro"],
            cidade=data["cidade"],
            estado=data["estado"]
        )

        return pessoa.to_dict(), 201

    except Exception as error:

        return {
            "error": str(error)
        }, 401


@pessoa_bp.route("/register", methods=["GET"])
def register_pessoa():
    return render_template("index.html")
