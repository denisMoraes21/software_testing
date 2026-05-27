from flask import Flask
from app.database import Database
from enum import StrEnum


class DatabaseConfig(StrEnum):
    URI = "SQLALCHEMY_DATABASE_URI"
    MODIFICATIONS = "SQLALCHEMY_TRACK_MODIFICATIONS"

    DATABASE_FILE = "app"
    DATABASE_URI = f"sqlite:///{DATABASE_FILE}.db"


class App:
    _class_instance = None
    _app_instance = None

    @classmethod
    def get_instance(cls):
        return cls._class_instance

    @classmethod
    def set_instance(cls, class_instance):
        cls._class_instance = class_instance

    @classmethod
    def get_app(cls):
        return cls._app_instance

    @classmethod
    def set_app(cls, app_object):
        cls._app_instance = app_object

    def __new__(cls):
        if cls.get_instance() is None:
            cls.set_instance(super(App, cls).__new__(cls))
            cls.set_app(Flask(__name__))

            _app = cls.get_app()
            _app.config[DatabaseConfig.URI] = DatabaseConfig.DATABASE_URI
            _app.config[DatabaseConfig.MODIFICATIONS] = False

            _database = Database().get_db()
            _database.init_app(_app)

            with _app.app_context():
                _database.create_all()

        return cls.get_instance()
