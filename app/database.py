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


db = Database().get_db()


# class Pessoa(db.Model):
#
#     __tablename__ = "pessoas"
#
#     id = db.Column(db.Integer, primary_key=True)
#
#     nome_completo = db.Column(
#         db.String(150),
#         nullable=False
#     )
#
#     cpf = db.Column(
#         db.String(14),
#         unique=True,
#         nullable=False
#     )
#
#     data_nascimento = db.Column(
#         db.String(10),
#         nullable=False
#     )
#
#     sexo = db.Column(
#         db.String(20),
#         nullable=False
#     )
#
#     estado_civil = db.Column(
#         db.String(30),
#         nullable=False
#     )
#
#     nacionalidade = db.Column(
#         db.String(50),
#         nullable=False
#     )
#
#     def __repr__(self):
#         return f"<Pessoa {self.nome_completo}>"