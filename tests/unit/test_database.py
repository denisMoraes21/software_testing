import unittest
from app.database import Database
from unittest.mock import Mock, patch
from app.app import App


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.app = App().get_app()
        self.client = self.app.test_client()

    def test_singleton(self):
        db_1 = Database().get_db()
        db_2 = Database().get_db()
        self.assertEqual(db_1, db_2)

    @patch("app.data.services.user_service.UserService.create_user")
    def test_create_user(self, mock_create_user):

        user_mock = Mock()

        user_mock.to_dict.return_value = {
            "id": 1,
            "name": "Lucas"
        }

        mock_create_user.return_value = user_mock

        payload = {
            "name": "Lucas"
        }

        response = self.client.post(
            "/users/create",
            json=payload
        )

        self.assertEqual(response.status_code, 201)

        mock_create_user.assert_called_once_with(
            name="Lucas"
        )
