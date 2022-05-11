from flask import Blueprint, request
from medium_scraper import autocomplete, Config
from medium_scraper.word_checker.app_helper import *

word_checker = Blueprint('word_checker', __name__)


@word_checker.route('/typo_check/<string:word>')
def typo_checker(word):
    return check_typo(word)


if Config.RUN_AUTOCOMPLETER:

    @word_checker.route('/auto_complete', websocket=True)
    def auto_completer():
        return autocompleter(request)

    @word_checker.route('/insert_autocomplete_word/<string:tag>')
    def insert_auto_complete_word(tag):
        autocomplete.insert_word(tag)
        return ""