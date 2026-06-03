from validate_docbr import CPF
from app.data.repositories.pessoas_repository import PessoaRepository


class PessoaService:

    @staticmethod
    def create_pessoa(**dados):

        validador_cpf = CPF()

        if not validador_cpf.validate(
                dados["cpf"]
        ):
            print("cpf invalido")
            raise Exception(
                "CPF inválido"
            )

        pessoa_existente = PessoaRepository.get_by_cpf(
            dados["cpf"]
        )

        if pessoa_existente:
            raise Exception(
                "CPF já cadastrado"
            )

        email_existente = PessoaRepository.get_by_email(
            dados["email"]
        )

        if email_existente:
            raise Exception(
                "E-mail já cadastrado"
            )

        return PessoaRepository.create(
            **dados
        )