class Trie(object):
    def __init__(self, words):
        """
        Initialise the class.

        :arg list words: List of words.
        """
        self.root = {}

        self._build(words)

    def _build(self, words):
        """
        Build the trie.

        :arg list words: List of words.
        """
        for word in words:
            self.add(word)

    def _find(self, word):
        """
        Find the node after following the path in the trie given by {word}.

        :arg str word: A word.

        :returns dict: The node if found, None otherwise.
        """
        node = self.root

        for char in word:
            if char not in node:
                return {}
            node = node[char]

        return node

    def __contains__(self, word):
        return '' in self._find(word)

    def add(self, word):
        """
        Add a word to the trie.

        :arg str word: A word.
        """
        node = self.root

        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]

        node[''] = {}

    def has_prefix(self, word):
        return self._find(word) != {}
