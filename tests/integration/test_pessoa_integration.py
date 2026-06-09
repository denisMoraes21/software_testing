import unittest
from app.app import App
from app.database import db
from app.data.models.pessoas_model import PessoaModel


class TestPessoaIntegration(unittest.TestCase):

    def setUp(self):
        self.app = App().get_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            PessoaModel.query.delete()
            db.session.commit()

        self.payload = {
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

    def test_cpf_invalido(self):
        payload = self.payload.copy()
        payload["cpf"] = "12345678900"

        response = self.client.post(
            "/pessoas/create",
            json=payload
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "CPF inválido"
        )

    def test_email_invalido(self):
        payload = self.payload.copy()
        payload["email"] = "joao@gmail"

        response = self.client.post(
            "/pessoas/create",
            json=payload
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "E-mail inválido"
        )

    def test_cep_invalido(self):
        payload = self.payload.copy()
        payload["cep"] = "123"

        response = self.client.post(
            "/pessoas/create",
            json=payload
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "CEP inválido"
        )

    def test_nome_sem_sobrenome(self):
        payload = self.payload.copy()
        payload["nome_completo"] = "Joao"

        response = self.client.post(
            "/pessoas/create",
            json=payload
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "Informe nome e sobrenome"
        )

    def test_create_pessoa_sucesso(self):
        payload = self.payload.copy()
        payload["cpf"] = "11144477735"
        payload["email"] = "sucesso@gmail.com"

        response = self.client.post(
            "/pessoas/create",
            json=payload
        )

        self.assertEqual(response.status_code, 201)

    def test_cpf_ja_cadastrado(self):
        payload = self.payload.copy()

        payload["cpf"] = "39053344705"
        payload["email"] = "primeiro@gmail.com"

        self.client.post(
            "/pessoas/create",
            json=payload
        )

        payload["email"] = "segundo@gmail.com"

        response = self.client.post(
            "/pessoas/create",
            json=payload
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "CPF já cadastrado"
        )

    def test_email_ja_cadastrado(self):
        payload = self.payload.copy()

        payload["cpf"] = "11144477735"
        payload["email"] = "duplicado@gmail.com"

        self.client.post(
            "/pessoas/create",
            json=payload
        )

        payload["cpf"] = "39053344705"

        response = self.client.post(
            "/pessoas/create",
            json=payload
        )

        self.assertEqual(response.status_code, 401)

        self.assertEqual(
            response.get_json()["error"],
            "E-mail já cadastrado"
        )