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
autocomplete = AutoComplete()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    spellChecker.init_spell_checker()
    if Config.RUN_AUTOCOMPLETER:
        print('building trie')
        autocomplete.init_trie(file_handler)

    from medium_scraper.routes import main
    from medium_scraper.word_helper.app import word_helper
    app.register_blueprint(main)
    app.register_blueprint(word_helper)

    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

    CORS(app)
    print('returning app')
    return app