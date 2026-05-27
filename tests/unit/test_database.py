import unittest
from app.database import Database


class TestDatabase(unittest.TestCase):

    def test_singleton(self):
        db_1 = Database().get_db()
        db_2 = Database().get_db()
        self.assertEqual(db_1, db_2)
