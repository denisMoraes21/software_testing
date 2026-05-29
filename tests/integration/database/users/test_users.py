import unittest
import requests


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = "http://127.0.0.1:5000"
        self.PREFIX_ENDPOINT = "/users"
        self.CREATE_USER_ENDPOINT = f"{self.PREFIX_ENDPOINT}/create"
        self.DELETE_USER_ENDPOINT = f"{self.PREFIX_ENDPOINT}/delete"
        self.REGISTER_PAGE_ENDPOINT = f"{self.PREFIX_ENDPOINT}/register"

    def test_create_user(self):
        _body = {
            "name": "Denis"
        }

        _response = requests.post(
            f"{self.BASE_URL}{self.CREATE_USER_ENDPOINT}",
            json=_body
        )

        self.assertEqual(_response.status_code, 201)
        self.assertNotEqual(_response.json(), _body)

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
