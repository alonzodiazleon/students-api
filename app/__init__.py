from flask import Flask
from app.database import init_db
from app.routes.student_routes import student_bp


def create_app():
    app = Flask(__name__)

    init_db()

    app.register_blueprint(student_bp)

    return app