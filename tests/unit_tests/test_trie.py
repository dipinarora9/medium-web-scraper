import os
from medium_scraper.word_checker.models.trie import Trie


def test_new_trie():
    """
    GIVEN a Trie model
    WHEN a new Trie is created
    THEN check that its fields are defined correctly
    """
    trie = Trie()
    trie.insert("abc")
    assert trie.search("abc") == True
    assert trie.search("ab") == False
    assert trie.suggest_next_word("a") == ["abc"]
    assert trie.suggest_next_word("ab") == ["abc"]
    assert trie.suggest_next_word("c") == []


# BASE_PATH = os.path.dirname(__file__)
#     with open(os.path.join(BASE_PATH, 'words.txt'), 'r') as word_file:
#         valid_words = set(word_file.read().split())
#     for word in valid_words:
#         trie.insert(word.lower())