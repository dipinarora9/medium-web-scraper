from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from medium_scraper.config import Config
from medium_scraper.services.file_handler_service import FileHandler
from medium_scraper.services.spell_checker_service import SpellChecker
from medium_scraper.services.autocomplete_service import AutoComplete

app = Flask(__name__)

db = SQLAlchemy()
file_handler = FileHandler()
spellChecker = SpellChecker()
autocomplete = AutoComplete()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    if Config.RUN_AUTOCOMPLETER:
        print('building trie')
        file_handler.init_file_handler()
        autocomplete.init_trie(file_handler)
        print('trie built')
    else:
        file_handler.init_file_handler()
        spellChecker.init_spell_checker(file_handler)
        db.init_app(app)

    from medium_scraper.main import homepage
    from medium_scraper.posts.app import posts
    from medium_scraper.word_checker.app import word_checker

    app.register_blueprint(word_checker)
    app.register_blueprint(posts)
    app.register_blueprint(homepage)

    # with app.app_context():
    #     if not Config.RUN_AUTOCOMPLETER:
    #         db.drop_all()
    #         db.create_all()

    CORS(app)
    return app