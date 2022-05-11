from medium_scraper.helpers.constants import WORDS_FILE_LOCATION


class FileHandler:

    def init_file_handler(self):
        with open(WORDS_FILE_LOCATION) as word_file:
            valid_words = set(word_file.read().split())

        self.words = valid_words
