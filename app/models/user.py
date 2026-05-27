from app.database import Database


class User(Database.Model):

    id = Database.Column(Database.Integer, primary_key=True)
    name = Database.Column(Database.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
