def _hamming(path, node, word, distance):
    """
    Find the first path in the trie that is within a certain hamming distance
    of {word}. Note that this does not necessarily the one with the smallest
    distance.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.
    :arg str word: Query word.
    :arg int distance: Amount of errors we can still make.

    :returns str: A word in the trie that has Hamming distance of at most
        {distance} to {word}.
    """
    if distance < 0:
        return ''
    if not word:
        if '' in node:
            return path
        return ''

    car, cdr = word[0], word[1:]
    for char in node:
        result = _hamming(
            path + char, node[char], cdr, distance - int(char != car))
        if result:
            return result

    return ''


def _edit(path, node, word, distance):
    pass


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

        :returns dict: The node if found, {} otherwise.
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

    def hamming(self, word, distance):
        return _hamming('', self.root, word, distance)

    def best_hamming(self, word, distance):
        """
        Find the best match with {word} in the trie.

        :arg str word: Query word.
        :arg int distance: Amount of errors we can still make.

        :returns str: Best match with {word}.
        """
        if word in self:
            return word

        for i in range(1, distance + 1):
            result = self.hamming(word, i)
            if result:
                return result

        return ''

    def edit(self, word, distance):
        return _edit('', self.root, word, distance)
