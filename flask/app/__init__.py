from flask import Flask
from app.db import init_db

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    with app.app_context():
        init_db()

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
