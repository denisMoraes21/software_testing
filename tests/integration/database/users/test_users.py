import unittest
import requests

from app.app import App
from app.data.repositories.user_repository import UserRepository
from app.data.models.user_model import UserModel


class TestUsers(unittest.TestCase):
    def setUp(self):
        App()

        self.app = App.get_app()
        self.BASE_URL = "http://127.0.0.1:5000"
        self.PREFIX_ENDPOINT = "/users"
        self.CREATE_USER_ENDPOINT = f"{self.PREFIX_ENDPOINT}/create"
        self.DELETE_USER_ENDPOINT = f"{self.PREFIX_ENDPOINT}/delete"
        self.REGISTER_PAGE_ENDPOINT = f"{self.PREFIX_ENDPOINT}/register"

    def test_create_user_http(self):
        _body = {
            "name": "Denis"
        }

        _response = requests.post(
            f"{self.BASE_URL}{self.CREATE_USER_ENDPOINT}",
            json=_body
        )

        self.assertEqual(_response.status_code, 201)
        self.assertNotEqual(_response.json(), _body)

    def test_create_user_database(self):
        with self.app.app_context():

            user = UserRepository.create(
                name="Lucas"
            )

            self.assertIsNotNone(user.id)

            db_user = UserModel.query.filter_by(
                name="Lucas"
            ).first()

            self.assertIsNotNone(db_user)

            self.assertEqual(db_user.name, "Lucas")

    def test_register(self):
        _response = requests.get(
            f"{self.BASE_URL}{self.REGISTER_PAGE_ENDPOINT}"
        )
        self.assertEqual(_response.status_code, 200)

    def tearDown(self):
        _body = {
            "id": 1
        }

        requests.post(
            f"{self.BASE_URL}{self.DELETE_USER_ENDPOINT}",
            json=_body
        )
