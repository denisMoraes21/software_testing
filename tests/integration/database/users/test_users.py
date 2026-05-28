import unittest
import requests


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.BASE_URL = "http://127.0.0.1:5000"

    def test_create_user(self):
        _body = {
            "name": "Denis"
        }
        _response = requests.post(
            f"{self.BASE_URL}/api/create_users",
            json=_body
        )
        self.assertEqual(_response.status_code, 201)
        self.assertNotEqual(_response.json(), _body)

    def tearDown(self):
        _body = {
            "id": 1
        }
        requests.post(f"{self.BASE_URL}/api/delete_users", json=_body)
