class TrieNode:

    # Trie node class
    def __init__(self):
        self.children = dict()
        self.score = 0
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
        pCrawl.score += 1

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

        return pCrawl.score

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
        suggestions = dict()

        # suggestion logic
        for k, v in pCrawl.children.items():
            if v.score:
                suggestions[key + k] = v.score

        for k, v in pCrawl.children.items():
            for sub_child_k, sub_child_v in v.children.items():
                if sub_child_v.score:
                    suggestions[key + k + sub_child_k] = sub_child_v.score
                for sub_sub_child_k, sub_sub_child_v in sub_child_v.children.items(
                ):
                    if sub_sub_child_v.score:
                        suggestions[key + k + sub_child_k +
                                    sub_sub_child_k] = sub_sub_child_v.score

        suggestions = sorted(suggestions.keys(),
                             key=lambda x: suggestions[x],
                             reverse=True)

        return suggestions[:5]
