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

        for character in word:
            if character not in node:
                return {}
            node = node[character]

        return node

    def __contains__(self, word):
        if '' in self._find(word):
            return True
        return False

    def add(self, word):
        """
        Add a word to the trie.
        """
        node = self.root

        for character in word:
            if character not in node:
                node[character] = {}
            node = node[character]

        node[''] = {}

    def has_prefix(self, word):
        if self._find(word) != {}:
            return True
        return False
