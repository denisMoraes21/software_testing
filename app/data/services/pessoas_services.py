from datetime import datetime

from validate_docbr import CPF

from app.data.repositories.pessoas_repository import (
    PessoaRepository
)


class PessoaService:

    @staticmethod
    def create_pessoa(**dados):

        # Nome completo

        nome = dados["nome_completo"].strip()

        if len(nome) < 5:
            raise Exception(
                "Nome muito curto"
            )

        if " " not in nome:
            raise Exception(
                "Informe nome e sobrenome"
            )

        if any(
            char.isdigit()
            for char in nome
        ):
            raise Exception(
                "Nome não pode conter números"
            )

        # Estado civil

        if not dados["estado_civil"]:
            raise Exception(
                "Selecione um estado civil"
            )

        # Data de nascimento

        data_nascimento = datetime.strptime(
            dados["data_nascimento"],
            "%Y-%m-%d"
        )

        if data_nascimento > datetime.now():
            raise Exception(
                "Data de nascimento inválida"
            )

        # E-mail

        email = dados["email"].strip()

        if (
            "@" not in email
            or email.startswith("@")
            or email.endswith("@")
        ):
            raise Exception(
                "E-mail inválido"
            )

        # Telefone

        telefone = (
            dados["telefone"]
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if (
            not telefone.isdigit()
            or len(telefone) < 10
        ):
            raise Exception(
                "Telefone inválido"
            )

        # Celular

        celular = (
            dados["celular"]
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )

        if (
            not celular.isdigit()
            or len(celular) < 11
        ):
            raise Exception(
                "Celular inválido"
            )

        # CEP

        cep = dados["cep"].replace(
            "-",
            ""
        )

        if (
            not cep.isdigit()
            or len(cep) != 8
        ):
            raise Exception(
                "CEP inválido"
            )

        # UF

        ufs = [
            "AC", "AL", "AP", "AM", "BA",
            "CE", "DF", "ES", "GO", "MA",
            "MT", "MS", "MG", "PA", "PB",
            "PR", "PE", "PI", "RJ", "RN",
            "RS", "RO", "RR", "SC", "SP",
            "SE", "TO"
        ]

        if (
            dados["estado"]
            .upper()
            not in ufs
        ):
            raise Exception(
                "UF inválida"
            )

        # CPF

        validador_cpf = CPF()

        if not validador_cpf.validate(
            dados["cpf"]
        ):
            raise Exception(
                "CPF inválido"
            )

        # CPF já cadastrado

        pessoa_existente = (
            PessoaRepository.get_by_cpf(
                dados["cpf"]
            )
        )

        if pessoa_existente:
            raise Exception(
                "CPF já cadastrado"
            )

        # E-mail já cadastrado

        email_existente = (
            PessoaRepository.get_by_email(
                dados["email"]
            )
        )

        if email_existente:
            raise Exception(
                "E-mail já cadastrado"
            )

        return PessoaRepository.create(
            **dados
        )