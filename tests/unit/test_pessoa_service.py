import unittest
from unittest.mock import patch, Mock
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
            "telefone": "9233334444",
            "celular": "92999998888",
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
        dados = self.dados.copy()
        dados["nome_completo"] = "J S"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Nome muito curto"
        )

    def test_nome_sem_sobrenome(self):
        dados = self.dados.copy()
        dados["nome_completo"] = "Joao"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Informe nome e sobrenome"
        )

    def test_nome_com_numero(self):
        dados = self.dados.copy()
        dados["nome_completo"] = "Joao123 Silva"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Nome não pode conter números"
        )

    def test_estado_civil_vazio(self):
        dados = self.dados.copy()
        dados["estado_civil"] = ""

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Selecione um estado civil"
        )

    def test_data_nascimento_futura(self):
        dados = self.dados.copy()
        dados["data_nascimento"] = "2050-01-01"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Data de nascimento inválida"
        )

    def test_email_invalido(self):
        dados = self.dados.copy()
        dados["email"] = "joao@gmail"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "E-mail inválido"
        )

    def test_telefone_invalido(self):
        dados = self.dados.copy()
        dados["telefone"] = "123"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Telefone inválido"
        )

    def test_celular_invalido(self):
        dados = self.dados.copy()
        dados["celular"] = "123"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Celular inválido"
        )

    def test_cep_invalido(self):
        dados = self.dados.copy()
        dados["cep"] = "123"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "CEP inválido"
        )

    def test_uf_invalida(self):
        dados = self.dados.copy()
        dados["estado"] = "XX"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "UF inválida"
        )

    def test_cpf_invalido(self):
        dados = self.dados.copy()
        dados["cpf"] = "12345678900"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "CPF inválido"
        )

        # Novos add

    def test_cidade_invalida(self):
        dados = self.dados.copy()
        dados["cidade"] = "M1"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Cidade inválida"
            )

    def test_nacionalidade_invalida(self):
        dados = self.dados.copy()
        dados["nacionalidade"] = "Br4sil"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Nacionalidade inválida"
        )

    def test_bairro_invalido(self):
        dados = self.dados.copy()
        dados["bairro"] = "A"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Bairro inválido"
        )

    def test_logradouro_invalido(self):
        dados = self.dados.copy()
        dados["logradouro"] = "R"

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(**dados)

        self.assertEqual(
            str(context.exception),
            "Logradouro inválido"
        )

    @patch(
        "app.data.services.pessoas_services.PessoaRepository.get_by_cpf"
    )
    def test_cpf_ja_cadastrado(
            self,
            mock_get_by_cpf
    ):
        mock_get_by_cpf.return_value = Mock()

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(
                **self.dados
            )

        self.assertEqual(
            str(context.exception),
            "CPF já cadastrado"
        )


    @patch(
        "app.data.services.pessoas_services.PessoaRepository.get_by_email"
    )
    @patch(
        "app.data.services.pessoas_services.PessoaRepository.get_by_cpf"
    )
    def test_email_ja_cadastrado(
            self,
            mock_get_by_cpf,
            mock_get_by_email
    ):
        mock_get_by_cpf.return_value = None

        mock_get_by_email.return_value = Mock()

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(
                **self.dados
            )

        self.assertEqual(
            str(context.exception),
            "E-mail já cadastrado"
        )

    @patch(
        "app.data.services.pessoas_services.PessoaRepository.get_by_cpf"
    )
    def test_cpf_ja_cadastrado(
            self,
            mock_get_by_cpf
    ):
        mock_get_by_cpf.return_value = Mock()

        with self.assertRaises(Exception) as context:
            PessoaService.create_pessoa(
                **self.dados
            )

        self.assertEqual(
            str(context.exception),
            "CPF já cadastrado"
        )

    @patch(
        "app.data.services.pessoas_services.PessoaRepository.create"
    )
    @patch(
        "app.data.services.pessoas_services.PessoaRepository.get_by_email"
    )
    @patch(
        "app.data.services.pessoas_services.PessoaRepository.get_by_cpf"
    )
    def test_create_pessoa_sucesso(
            self,
            mock_get_by_cpf,
            mock_get_by_email,
            mock_create
    ):
        mock_get_by_cpf.return_value = None

        mock_get_by_email.return_value = None

        mock_create.return_value = Mock()

        resultado = PessoaService.create_pessoa(
            **self.dados
        )

        self.assertIsNotNone(
            resultado
        )

        mock_create.assert_called_once()