from app.data.repositories.base_repository import BaseRepository
from app.data.models.pessoas_model import PessoaModel


class PessoaRepository(BaseRepository):
    model = PessoaModel

    @classmethod
    def get_by_cpf(cls, cpf):
        return cls.model.query.filter_by(
            cpf=cpf
        ).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.model.query.filter_by(
            email=email
        ).first()

    @classmethod
    def get_by_nome(cls, nome):
        return cls.model.query.filter_by(
            nome_completo=nome
        ).first()
