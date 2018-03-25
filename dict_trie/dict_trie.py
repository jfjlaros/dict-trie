import itertools


def _add(root, word):
    """Add a word to a trie.

    :arg dict root: Root of the trie.
    :arg str word: A word.
    """
    node = root

    for char in word:
        if char not in node:
            node[char] = {}
        node = node[char]

    node[''] = {}


def _find(root, word):
    """Find the node after following the path in a trie given by {word}.

    :arg dict root: Root of the trie.
    :arg str word: A word.

    :returns dict: The node if found, {} otherwise.
    """
    node = root

    for char in word:
        if char not in node:
            return {}
        node = node[char]

    return node


def _remove(node, word):
    """Remove a word from a trie.

    :arg dict node: Current node.
    :arg str word: Word to be removed.

    :returns bool:
    """
    if not word:
        if '' in node:
            node.pop('')
            return True
        return False

    car, cdr = word[0], word[1:]
    if car not in node:
        return False

    result = _remove(node[car], cdr)
    if result:
        if not node[car]:
            node.pop(car)

    return result


def _iterate(path, node):
    """Convert a trie into a list.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.

    :returns iter: All words in a trie.
    """
    if '' in node:
        yield path

    for char in node:
        for result in _iterate(path + char, node[char]):
            yield result


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

    for char in alphabet:
        node[char] = {}
        _fill(node[char], alphabet, length - 1)


def _hamming(path, node, word, distance, cigar):
    """Find all paths in a trie that are within a certain hamming distance of
    {word}.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.
    :arg str word: Query word.
    :arg int distance: Amount of allowed errors.

    :returns iter: All word in a trie that have Hamming distance of at most
        {distance} to {word}.
    """
    if distance < 0:
        return
    if not word:
        if '' in node:
            yield (path, distance, cigar)
        return

    car, cdr = word[0], word[1:]
    for char in node:
        if char == car:
            penalty = 0
            operation = '='
        else:
            penalty = 1
            operation = 'X'
        for result in _hamming(
                path + char, node[char], cdr, distance - penalty,
                cigar + operation):
            yield result


def _levenshtein(path, node, word, distance, cigar):
    """Find all paths in a trie that are within a certain Levenshtein
    distance of {word}.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.
    :arg str word: Query word.
    :arg int distance: Amount of allowed errors.

    :returns iter: All word in a trie that have Hamming distance of at most
        {distance} to {word}.
    """
    if distance < 0:
        return
    if not word:
        if '' in node:
            yield (path, distance, cigar)
        car, cdr = '', ''
    else:
        car, cdr = word[0], word[1:]

    # Deletion.
    for result in _levenshtein(path, node, cdr, distance - 1, cigar + 'D'):
        yield result

    for char in node:
        # Substitution.
        if car:
            if char == car:
                penalty = 0
                operation = '='
            else:
                penalty = 1
                operation = 'X'
            for result in _levenshtein(
                    path + char, node[char], cdr, distance - penalty,
                    cigar + operation):
                yield result
        # Insertion.
        for result in _levenshtein(
                path + char, node[char], word, distance - 1, cigar + 'I'):
            yield result


class Trie(object):
    def __init__(self, words=None):
        """Initialise the class.

        :arg list words: List of words.
        """
        self.root = {}

        if words:
            for word in words:
                self.add(word)

    def __contains__(self, word):
        return '' in _find(self.root, word)

    def __iter__(self):
        return _iterate('', self.root)

    def add(self, word):
        _add(self.root, word)

    def remove(self, word):
        return _remove(self.root, word)

    def has_prefix(self, word):
        return _find(self.root, word) != {}

    def fill(self, alphabet, length):
        _fill(self.root, alphabet, length)

    def all_hamming_(self, word, distance):
        return itertools.imap(
            lambda x: (x[0], distance - x[1], x[2]),
            _hamming('', self.root, word, distance, ''))

    def all_hamming(self, word, distance):
        return itertools.imap(
            lambda x: x[0], _hamming('', self.root, word, distance, ''))

    def hamming(self, word, distance):
        try:
            return self.all_hamming(word, distance).next()
        except StopIteration:
            return ''

    def best_hamming(self, word, distance):
        """Find the best match with {word} in a trie.

        :arg str word: Query word.
        :arg int distance: Maximum allowed distance.

        :returns str: Best match with {word}.
        """
        if _find(self.root, word):
            return word

        for i in range(1, distance + 1):
            result = self.hamming(word, i)
            if result:
                return result

        return ''

    def all_levenshtein_(self, word, distance):
        return itertools.imap(
            lambda x: (x[0], distance - x[1], x[2]),
            _levenshtein('', self.root, word, distance, ''))

    def all_levenshtein(self, word, distance):
        return itertools.imap(
            lambda x: x[0], _levenshtein('', self.root, word, distance, ''))

    def levenshtein(self, word, distance):
        try:
            return self.all_levenshtein(word, distance).next()
        except StopIteration:
            return ''

    def best_levenshtein(self, word, distance):
        """Find the best match with {word} in a trie.

        :arg str word: Query word.
        :arg int distance: Maximum allowed distance.

        :returns str: Best match with {word}.
        """
        if _find(self.root, word):
            return word

        for i in range(1, distance + 1):
            result = self.levenshtein(word, i)
            if result:
                return result

        return ''
