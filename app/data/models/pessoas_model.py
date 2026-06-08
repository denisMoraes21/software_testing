from app.database import db
from app.data.models.base_model import BaseModel


class PessoaModel(BaseModel):
    __tablename__ = "pessoa"

    nome_completo = db.Column(
        db.String(150),
        nullable=False
    )

    cpf = db.Column(
        db.String(14),
        nullable=False,
        unique=True,
        index=True
    )

    data_nascimento = db.Column(
        db.String(10),
        nullable=False
    )

    sexo = db.Column(
        db.String(20),
        nullable=False
    )

    estado_civil = db.Column(
        db.String(30),
        nullable=False
    )

    nacionalidade = db.Column(
        db.String(50),
        nullable=False
    )

    # Dados de contato
    telefone = db.Column(
        db.String(20),
        nullable=True
    )

    celular = db.Column(
        db.String(20),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True,
        index=True
    )

    # Endereço
    cep = db.Column(
        db.String(9),
        nullable=False
    )

    logradouro = db.Column(
        db.String(150),
        nullable=False
    )

    numero = db.Column(
        db.String(20),
        nullable=False
    )

    complemento = db.Column(
        db.String(100),
        nullable=True
    )

    bairro = db.Column(
        db.String(100),
        nullable=False
    )

    cidade = db.Column(
        db.String(100),
        nullable=False
    )

    estado = db.Column(
        db.String(2),
        nullable=False
    )

    # Exclusão lógica
    ativo = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    def __repr__(self):
        return (
            f"<PessoaModel "
            f"id={self.id} "
            f"cpf='{self.cpf}' "
            f"nome='{self.nome_completo}'>"
        )
