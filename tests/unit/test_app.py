import unittest
from app.app import App


class TestApp(unittest.TestCase):

    def test_singleton(self):
        app_1 = App().get_app()
        app_2 = App().get_app()
        self.assertEqual(app_1, app_2)
