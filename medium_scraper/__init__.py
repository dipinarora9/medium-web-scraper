from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_ngrok import run_with_ngrok
from flask_cors import CORS
from medium_scraper.config import Config

app = Flask(__name__, template_folder='views')

db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from medium_scraper.routes import main
    app.register_blueprint(main)

    run_with_ngrok(app)
    CORS(app)
    return app