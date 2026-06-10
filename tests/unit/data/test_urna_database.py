import unittest
from unittest.mock import Mock, patch
from app.app import create_app


class TestUrnaDatabase(unittest.TestCase):

    def setUp(self):
        """Configura o cliente de testes do Flask (roda 100% em memória)"""
        self.app = create_app()
        self.client = self.app.test_client()


    # 1. TESTES DA ROTA: /api/eleitores (GET e POST)

    @patch("app.routes.urna_routes.get_db_connection")
    def test_cadastrar_eleitor_sucesso(self, mock_get_db):
        """POST /api/eleitores - Teste unitário de criação de eleitor com sucesso"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn

        payload = {"nome": "Adeilso Azevedo"}
        response = self.client.post("/api/eleitores", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("status"), "sucesso")

        # Valida se executou o INSERT correto
        mock_conn.execute.assert_called_once_with(
            'INSERT INTO eleitores (nome) VALUES (?)',
            ("Adeilso Azevedo",)
        )
        mock_conn.commit.assert_called_once()

    @patch("app.routes.urna_routes.get_db_connection")
    def test_listar_eleitores_sucesso(self, mock_get_db):
        """GET /api/eleitores - Teste unitário de listagem de todos os eleitores"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn

        # Simula o retorno de dados do SQLite no formato Row/Dicionário
        mock_eleitores = [
            {"id": 1, "nome": "Adeilso", "ja_votou": 0},
            {"id": 2, "nome": "Denis", "ja_votou": 1}
        ]
        mock_conn.execute.return_value.fetchall.return_value = mock_eleitores

        response = self.client.get("/api/eleitores")

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]["nome"], "Adeilso")
        mock_conn.execute.assert_called_once_with('SELECT * FROM eleitores')

    # 2. TESTES DA ROTA: /api/eleitores/<id> (PUT e DELETE)

    @patch("app.routes.urna_routes.get_db_connection")
    def test_alterar_nome_eleitor_sucesso(self, mock_get_db):
        """PUT /api/eleitores/<id> - Teste unitário de alteração de dados do eleitor"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn

        payload = {"nome": "Adeilso Melo"}
        response = self.client.put("/api/eleitores/1", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("status"), "sucesso")

        # Verifica se rodou o comando UPDATE com o ID correto na URL
        mock_conn.execute.assert_called_once_with(
            'UPDATE eleitores SET nome = ? WHERE id = ?',
            ("Adeilso Melo", 1)
        )
        mock_conn.commit.assert_called_once()

    @patch("app.routes.urna_routes.get_db_connection")
    def test_deletar_eleitor_sucesso(self, mock_get_db):
        """DELETE /api/eleitores/<id> - Teste unitário de remoção completa do eleitor"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn

        response = self.client.delete("/api/eleitores/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("status"), "sucesso")

        # Garante que apagou o eleitor e cascateou a limpeza removendo os votos dele
        mock_conn.execute.assert_any_call('DELETE FROM eleitores WHERE id = ?', (1,))
        mock_conn.execute.assert_any_call('DELETE FROM votos WHERE eleitor_id = ?', (1,))
        mock_conn.commit.assert_called_once()

    # 3. TESTES DA ROTA: /api/eleitores/<id>/encerrar (POST)

    @patch("app.routes.urna_routes.get_db_connection")
    def test_encerrar_votacao_eleitor(self, mock_get_db):
        """POST /api/eleitores/<id>/encerrar - Marca que o eleitor já concluiu a votação"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn

        response = self.client.post("/api/eleitores/1/encerrar")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("status"), "sucesso")

        # Valida se setou a flag ja_votou = 1 no banco
        mock_conn.execute.assert_called_once_with(
            'UPDATE eleitores SET ja_votou = 1 WHERE id = ?',
            (1,)
        )
        mock_conn.commit.assert_called_once()

    # 4. TESTES DA ROTA: /api/candidatos (GET com parâmetros de busca)

    @patch("app.routes.urna_routes.get_db_connection")
    def test_buscar_candidatos_por_cargo(self, mock_get_db):
        """GET /api/candidatos - Filtra candidatos de acordo com o cargo especificado"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn

        mock_retorno = [{"id": 5, "numero": "12", "nome": "João Silva", "cargo": "Prefeito"}]
        mock_conn.execute.return_value.fetchall.return_value = mock_retorno

        # Envia a requisição passando parâmetros de Query String (?cargo=Prefeito)
        response = self.client.get("/api/candidatos?cargo=Prefeito")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["nome"], "João Silva")
        mock_conn.execute.assert_called_once_with(
            'SELECT * FROM candidatos WHERE cargo = ?',
            ("Prefeito",)
        )

    # 5. TESTES DA ROTA: /api/votar (POST)

    @patch("app.routes.urna_routes.get_db_connection")
    def test_registrar_voto_sucesso(self, mock_get_db):
        """POST /api/votar - Computa um voto nominal da Urna"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn

        payload = {
            "eleitor_id": 2,
            "cargo": "Prefeito",
            "numero": "12",
            "tipo": "nominal"
        }

        response = self.client.post("/api/votar", json=payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("status"), "sucesso")

        # Confirma se capturou e mapeou o payload corretamente para as colunas do SQLite
        mock_conn.execute.assert_called_once_with(
            'INSERT INTO votos (eleitor_id, cargo, numero_candidato, tipo_voto) VALUES (?, ?, ?, ?)',
            (2, "Prefeito", "12", "nominal")
        )
        mock_conn.commit.assert_called_once()

    # 6. TESTES DA ROTA: /api/relatorio (GET Geral e GET Filtrado por Eleitor)

    @patch("app.routes.urna_routes.get_db_connection")
    def test_gerar_relatorio_geral(self, mock_get_db):
        """GET /api/relatorio - Consolida a contagem geral de todos os votos coletados"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.execute.return_value.fetchall.return_value = []

        response = self.client.get("/api/relatorio")

        self.assertEqual(response.status_code, 200)
        # Verifica se executou a Query complexa que agrupa por cargo com o GROUP BY
        self.assertIn("GROUP BY v.cargo", mock_conn.execute.call_args[0][0])

    @patch("app.routes.urna_routes.get_db_connection")
    def test_gerar_relatorio_especifico_eleitor(self, mock_get_db):
        """GET /api/relatorio?eleitor_id=<id> - Faz a auditoria de votos de um eleitor específico"""
        mock_conn = Mock()
        mock_get_db.return_value = mock_conn
        mock_conn.execute.return_value.fetchall.return_value = []

        response = self.client.get("/api/relatorio?eleitor_id=3")

        self.assertEqual(response.status_code, 200)
        # Garante que buscou usando o filtro WHERE v.eleitor_id = ?
        self.assertIn("WHERE v.eleitor_id = ?", mock_conn.execute.call_args[0][0])
        self.assertEqual(mock_conn.execute.call_args[0][1], ("3",))


if __name__ == '__main__':
    unittest.main()