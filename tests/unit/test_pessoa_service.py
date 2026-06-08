import unittest

from app.data.services.pessoas_services import PessoaService


class TestPessoaService(unittest.TestCase):

    def setUp(self):

        self.dados = {
            "nome_completo": "Joao Silva",
            "cpf": "52998224725",
            "data_nascimento": "2000-01-01",
            "sexo": "Masculino",
            "estado_civil": "Solteiro",
            "nacionalidade": "Brasileiro",
            "telefone": "123",
            "celular": "999999999",
            "email": "teste@gmail.com",
            "cep": "69050010",
            "logradouro": "Rua A",
            "numero": "10",
            "complemento": "",
            "bairro": "Centro",
            "cidade": "Manaus",
            "estado": "AM"
        }

    def test_nome_muito_curto(self):

        self.dados["nome_completo"] = "Ana"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**self.dados)

        self.assertEqual(
            str(context.exception),
            "Nome muito curto"
        )