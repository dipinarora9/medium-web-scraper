from threading import Thread
import requests
from medium_scraper.word_checker.models.trie import Trie
from medium_scraper.config import Config
from medium_scraper.helpers.constants import WORDS_FILE_LOCATION


class AutoComplete:

    def init_trie(self, file_handler):
        self._trie = Trie()

        # Construct trie
        for key in file_handler.words:
            self._trie.insert(key.lower())

    def insert_word(self, keyword):
        if Config.RUN_AUTOCOMPLETER:
            # with open(WORDS_FILE_LOCATION, 'a') as word_file:
            #     word_file.write(keyword + '\n')
            self._trie.insert(keyword.lower())
        else:
            thread = Thread(target=self.send_keyword_to_autocomplete_server,
                            kwargs={'keyword': keyword})
            thread.start()

    def send_keyword_to_autocomplete_server(self, keyword):
        try:
            autocomplete_server_url = Config.AUTO_COMPLETE_URL
            requests.get(autocomplete_server_url +
                         '/insert_autocomplete_word/' + keyword)
        except:
            pass

    def suggest_next_word(self, key):
        return self._trie.suggest_next_word(key)
