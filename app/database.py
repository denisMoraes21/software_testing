from flask_sqlalchemy import SQLAlchemy


class Database:

    _class_instance = None
    _database_instance = None

    @classmethod
    def get_instance(cls):
        return cls._class_instance

    @classmethod
    def set_instance(cls, class_object):
        cls._class_instance = class_object

    @classmethod
    def get_db(cls):
        return cls._database_instance

    @classmethod
    def set_db(cls, database_object):
        cls._database_instance = database_object

    def __new__(cls):
        if cls.get_instance() is None:
            cls.set_instance(super(Database, cls).__new__(cls))
            cls.set_db(SQLAlchemy())
        return cls.get_instance()


# Init database instance
db = Database().get_db()


if __name__ == "__main__":
    db_2 = Database().get_db()
    db_1 = Database().get_db()

    # Check singleton design
    assert db_1 == db_2
