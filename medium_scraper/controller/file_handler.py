import os


class FileHandler:
    BASE_PATH = os.path.dirname(__file__)

    def __init__(self):
        with open(os.path.join(FileHandler.BASE_PATH,
                               'words.txt')) as word_file:
            valid_words = set(word_file.read().split())

        self.words = valid_words