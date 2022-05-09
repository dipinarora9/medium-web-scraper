class TrieNode:

    # Trie node class
    def __init__(self):
        self.children = dict()

        # isEndOfWord is True if node represent the end of the word
        self.isEndOfWord = False
        self.suggestions = []


class Trie:

    # Trie data structure class
    def __init__(self):
        self.root = self.getNode()

    def getNode(self):

        # Returns new trie node (initialized to NULLs)
        return TrieNode()

    def insert(self, key):

        # If not present, inserts key into trie
        # If the key is prefix of trie node,
        # just marks leaf node
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            char = key[level]

            # if current character is not present
            if char not in pCrawl.children:
                pCrawl.children[char] = self.getNode()
            pCrawl = pCrawl.children[char]

        # mark last node as leaf
        pCrawl.isEndOfWord = True

    def search(self, key):

        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            char = key[level]
            if char not in pCrawl.children:
                return False
            pCrawl = pCrawl.children[char]

        return pCrawl.isEndOfWord

    def suggest_next_word(self, key):

        # Search key in the trie
        # Returns true if key presents
        # in trie, else false
        pCrawl = self.root
        length = len(key)
        for level in range(length):
            char = key[level]
            if char not in pCrawl.children:
                return []
            pCrawl = pCrawl.children[char]

        return pCrawl.isEndOfWord


def load_words():
    with open(
            'E:\Projects\GITHUB\medium-web-scraper\medium_scraper\controller\words.txt'
    ) as word_file:
        valid_words = set(word_file.read().split())

    return valid_words


if __name__ == "__main__":
    english_words = load_words()

    t = Trie()

    # Construct trie
    for key in english_words:
        t.insert(key)

    print("words inserted")
    # while True:
    #     wor = input("word: ")
    #     print(t.search(wor))
