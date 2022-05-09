from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from medium_scraper.config import Config
from medium_scraper.controller.spell_checker import SpellChecker

app = Flask(__name__, template_folder='views')

db = SQLAlchemy()
spellChecker = SpellChecker()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    spellChecker.init_spell_checker()

    from medium_scraper.routes import main
    from medium_scraper.word_helper.app import word_helper
    app.register_blueprint(main)
    app.register_blueprint(word_helper)

    CORS(app)
    return app