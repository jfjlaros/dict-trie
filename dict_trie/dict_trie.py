def _fill(node, alphabet, length):
    """Make a full trie using the characters in {alphabet}.

    :arg dict node: Current node.
    :arg tuple alphabet: Used alphabet.
    :arg int length: Length of the words to be generated.

    :returns iter: Trie containing all words of length {length} over alphabet
        {alphabet}.
    """
    if not length:
        node[''] = {}
        return

    for car in alphabet:
        node[car] = {}
        _fill(node[car], alphabet, length - 1)


def _to_list(path, node):
    """Convert a trie into a list.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.

    :returns iter: All words in the trie.
    """
    if '' in node:
        yield path

    for car in node:
        for result in _to_list(path + car, node[car]):
            yield result


def _hamming(path, node, word, distance):
    """Find all paths in the trie that are within a certain hamming distance of
    {word}.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.
    :arg str word: Query word.
    :arg int distance: Amount of allowed errors.

    :returns iter: All word in the trie that have Hamming distance of at most
        {distance} to {word}.
    """
    if distance < 0:
        return
    if not word:
        if '' in node:
            yield path
        return

    car, cdr = word[0], word[1:]
    for char in node:
        for result in _hamming(
            path + char, node[char], cdr, distance - int(char != car)):
            yield result


def _levenshtein(path, node, word, distance):
    """Find all paths in the trie that are within a certain Levenshtein
    distance of {word}.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.
    :arg str word: Query word.
    :arg int distance: Amount of allowed errors.

    :returns iter: All word in the trie that have Hamming distance of at most
        {distance} to {word}.
    """
    if distance < 0:
        return
    if not word:
        if '' in node:
            yield path
        return

    car, cdr = word[0], word[1:]

    # Deletion.
    for result in _levenshtein(path, node, cdr, distance - 1):
        yield result

    for char in node:
        # Substitution and insertion.
        for result in _levenshtein(
                path + char, node[char], cdr, distance - int(char != car)):
            yield result
        for result in _levenshtein(
                path + char, node[char], word, distance - 1):
            yield result


class Trie(object):
    def __init__(self, words=None):
        """Initialise the class.

        :arg list words: List of words.
        """
        self.root = {}

        if words:
            self._build(words)

    def _build(self, words):
        """Build the trie.

        :arg list words: List of words.
        """
        for word in words:
            self.add(word)

    def _find(self, word):
        """Find the node after following the path in the trie given by {word}.

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
        """Add a word to the trie.

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

    def fill(self, alphabet, length):
        _fill(self.root, alphabet, length)

    def to_list(self):
        return _to_list('', self.root)

    def all_hamming(self, word, distance):
        return _hamming('', self.root, word, distance)

    def hamming(self, word, distance):
        try:
            return self.all_hamming(word, distance).next()
        except StopIteration:
            return ''

    def best_hamming(self, word, distance):
        """Find the best match with {word} in the trie.

        :arg str word: Query word.
        :arg int distance: Maximum allowed distance.

        :returns str: Best match with {word}.
        """
        if word in self:
            return word

        for i in range(1, distance + 1):
            result = self.hamming(word, i)
            if result:
                return result

        return ''

    def all_levenshtein(self, word, distance):
        return _levenshtein('', self.root, word, distance)

    def levenshtein(self, word, distance):
        try:
            return self.all_levenshtein(word, distance).next()
        except StopIteration:
            return ''

    def best_levenshtein(self, word, distance):
        """Find the best match with {word} in the trie.

        :arg str word: Query word.
        :arg int distance: Maximum allowed distance.

        :returns str: Best match with {word}.
        """
        if word in self:
            return word

        for i in range(1, distance + 1):
            result = self.levenshtein(word, i)
            if result:
                return result

        return ''
