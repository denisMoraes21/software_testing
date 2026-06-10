import unittest
import requests

from app.app import create_app
from app.database import get_db_connection


class TestUrnaIntegration(unittest.TestCase):
    def setUp(self):
        # Inicializa o app Flask para os testes
        self.app = create_app()
        self.BASE_URL = "http://127.0.0.1:5000"

        # Endpoints reais mapeados do seu urna_routes.py
        self.ELEITORES_ENDPOINT = "/api/eleitores"
        self.VOTAR_ENDPOINT = "/api/votar"

    def test_gerenciar_eleitores_http(self):
        """Testa o cadastro de um novo eleitor via requisição POST HTTP"""
        # Nome único para evitar erros de restrição UNIQUE no banco
        nome_teste = "Eleitor Integracao Teste"
        _body = {
            "nome": nome_teste
        }

        try:
            _response = requests.post(
                f"{self.BASE_URL}{self.ELEITORES_ENDPOINT}",
                json=_body
            )

            # Verifica se retornou sucesso na requisição
            self.assertEqual(_response.status_code, 200)
            self.assertEqual(_response.json().get('status'), 'sucesso')

            # INTEGRAÇÃO COM BANCO: Verifica se o registro realmente entrou no SQLite
            conn = get_db_connection()
            eleitor = conn.execute('SELECT * FROM eleitores WHERE nome = ?', (nome_teste,)).fetchone()
            conn.close()

            self.assertIsNotNone(eleitor)
            self.assertEqual(eleitor['nome'], nome_teste)

        except requests.exceptions.ConnectionError:
            self.fail("O servidor Flask não está rodando! Execute 'python run.py' em outro terminal.")

    def test_registrar_voto_http(self):
        """Testa o fluxo de salvar voto associado a um eleitor"""
        _body = {
            "eleitor_id": 1,
            "cargo": "Prefeito",
            "numero": "12",
            "tipo": "nominal"
        }

        try:
            _response = requests.post(
                f"{self.BASE_URL}{self.VOTAR_ENDPOINT}",
                json=_body
            )

            self.assertEqual(_response.status_code, 200)
            self.assertEqual(_response.json().get('status'), 'sucesso')

            # INTEGRAÇÃO COM BANCO: Garante que o voto está gravado na tabela
            conn = get_db_connection()
            voto = conn.execute(
                'SELECT * FROM votos WHERE eleitor_id = ? AND cargo = ? AND numero_candidato = ?',
                (1, "Prefeito", "12")
            ).fetchone()
            conn.close()

            self.assertIsNotNone(voto)
            self.assertEqual(voto['tipo_voto'], 'nominal')

        except requests.exceptions.ConnectionError:
            self.fail("O servidor Flask não está rodando! Execute 'python run.py' em outro terminal.")

    def tearDown(self):
        # Limpa o eleitor de teste para não quebrar execuções futuras pelo parâmetro UNIQUE
        conn = get_db_connection()
        conn.execute("DELETE FROM eleitores WHERE nome = ?", ("Eleitor Integracao Teste",))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    unittest.main()