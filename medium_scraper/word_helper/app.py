import json
import simple_websocket
from flask import Blueprint, jsonify, request
from medium_scraper import spellChecker, autocomplete
from medium_scraper.config import Config

word_helper = Blueprint('word_helper', __name__)


@word_helper.route('/typo_check/<string:word>')
def typo_checker(word):
    typo_fix = spellChecker.correction(word)
    return jsonify(typo_fix)


if Config.RUN_AUTOCOMPLETER:

    @word_helper.route('/auto_complete', websocket=True)
    def auto_completer():
        ws = simple_websocket.Server(request.environ)
        try:
            while True:
                keyword = ws.receive()
                suggestions = autocomplete.suggest_next_word(keyword)
                ws.send(json.dumps(suggestions))
        except (KeyboardInterrupt, EOFError):
            ws.close()
            print('closing connection')
        except simple_websocket.ConnectionClosed:
            print('connection closed')
        except Exception as e:
            ws.close()
            print('closing connection due to ' + e)
        return ""

    @word_helper.route('/insert_autocomplete_word/<string:tag>')
    def insert_auto_complete_word(tag):
        autocomplete.insert_word(tag)
        return ""