# app/app.py
from flask import Flask, render_template
from app.database import init_db
from app.routes.urna_routes import urna_bp

def create_app():
    app = Flask(__name__)
    init_db() # Garante que o banco e as tabelas existem

    # Registra as rotas
    app.register_blueprint(urna_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app