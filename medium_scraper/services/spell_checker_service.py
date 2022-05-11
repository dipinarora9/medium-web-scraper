'''
NOTE: 
The following algorithm is authored by Peter Norvig
http://norvig.com/spell-correct.html
'''

import re
from collections import Counter


class SpellChecker:

    def init_spell_checker(self, file_handler):
        self.WORDS = Counter(file_handler.words)

    def P(self, word, N=None):
        if N is None:
            N = sum(self.WORDS.values())
        "Probability of `word`."
        return self.WORDS[word] / N

    def correction(self, word):
        "Most probable spelling correction for word."
        return max(self.candidates(word), key=self.P)

    def known(self, words):
        "The subset of `words` that appear in the dictionary of WORDS."
        return set(w for w in words if w in self.WORDS)

    def candidates(self, word):
        "Generate possible spelling corrections for word."
        return (self.known([word]) or self.known(self.edits1(word))
                or self.known(self.edits2(word)) or [word])

    @staticmethod
    def edits1(word):
        "All edits that are one edit away from `word`."
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    @staticmethod
    def edits2(word):
        "All edits that are two edits away from `word`."
        return (e2 for e1 in SpellChecker.edits1(word)
                for e2 in SpellChecker.edits1(e1))

    @staticmethod
    def words(text):
        return re.findall(r'\w+', text.lower())
