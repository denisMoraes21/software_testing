from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


# Criar banco automaticamente
with app.app_context():
    db.create_all()


# Rota principal
@app.route("/")
def home():
    return "Flask funcionando!"


# Criar usuário
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    user = User(name=data["name"])

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


# Listar usuários
@app.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()

    return jsonify([u.to_dict() for u in users])


if __name__ == "__main__":
    app.run(debug=True)