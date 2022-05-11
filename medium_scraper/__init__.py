from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from medium_scraper.config import Config
from medium_scraper.controller.file_handler import FileHandler
from medium_scraper.controller.spell_checker import SpellChecker
from medium_scraper.controller.autocomplete import AutoComplete

app = Flask(__name__, template_folder='views')

db = SQLAlchemy()
file_handler = FileHandler()
spellChecker = SpellChecker(file_handler)
autocomplete = AutoComplete(file_handler)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    print('Initializing spell checker')
    spellChecker.init_spell_checker()
    print('Initializing autocompleter')
    autocomplete.init_trie(file_handler)
    print('Initialization complete')

    from medium_scraper.routes import main
    from medium_scraper.word_helper.app import word_helper
    app.register_blueprint(main)
    app.register_blueprint(word_helper)

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    CORS(app)
    return app