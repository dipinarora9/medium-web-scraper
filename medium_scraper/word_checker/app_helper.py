import json
from flask import jsonify
import simple_websocket
from medium_scraper import autocomplete, spellChecker


def autocompleter(request):
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


def check_typo(word):
    typo_fix = spellChecker.correction(word)
    return jsonify(typo_fix)
