def _add(root: dict, word: str, count: int) -> None:
    """Add a word to a trie.

    :arg root: Root of the trie.
    :arg word: A word.
    :arg count: Multiplicity of `word`.
    """
    node = root

    for char in word:
        if char not in node:
            node[char] = {}
        node = node[char]

    if '' not in node:
        node[''] = 0
    node[''] += count


def _find(root: dict, word: str) -> dict:
    """Find the node after following the path in a trie given by {word}.

    :arg root: Root of the trie.
    :arg word: A word.

    :returns: The node if found, {} otherwise.
    """
    node = root

    for char in word:
        if char not in node:
            return {}
        node = node[char]

    return node


def _remove(node: dict, word: str, count: int) -> bool:
    """Remove a word from a trie.

    :arg node: Current node.
    :arg word: Word to be removed.
    :arg count: Multiplicity of `word`, force remove if this is -1.

    :returns: True if the last occurrence of `word` is removed.
    """
    if not word:
        if '' in node:
            node[''] -= count
            if node[''] < 1 or count == -1:
                node.pop('')
                return True
        return False

    car, cdr = word[0], word[1:]
    if car not in node:
        return False

    result = _remove(node[car], cdr, count)
    if result:
        if not node[car]:
            node.pop(car)

    return result


def _iterate(path: str, node: dict, unique: bool) -> iter:
    """Convert a trie into a list.

    :arg path: Path taken so far to reach the current node.
    :arg node: Current node.
    :arg unique: Do not list multiplicities.

    :returns: All words in a trie.
    """
    if '' in node:
        if not unique:
            for _ in range(1, node['']):
                yield path
        yield path

    for char in node:
        if char:
            for result in _iterate(path + char, node[char], unique):
                yield result


def _fill(node: dict, alphabet: tuple, length: int) -> iter:
    """Make a full trie using the characters in {alphabet}.

    :arg node: Current node.
    :arg alphabet: Used alphabet.
    :arg length: Length of the words to be generated.

    :returns: Trie containing all words of length {length} over alphabet
        {alphabet}.
    """
    if not length:
        node[''] = 1
        return

    for char in alphabet:
        node[char] = {}
        _fill(node[char], alphabet, length - 1)


def _hamming(
        path: str, node: dict, word: str, distance: int, cigar: str) -> iter:
    """Find all paths in a trie that are within a certain hamming distance of
    {word}.

    :arg path: Path taken so far to reach the current node.
    :arg node: Current node.
    :arg word: Query word.
    :arg distance: Amount of allowed errors.
    :arg cigar: CIGAR string.

    :returns: All words in a trie that have Hamming distance of at most
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
        if char:
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


def _levenshtein(
        path: str, node: dict, word: str, distance: int, cigar: str) -> iter:
    """Find all paths in a trie that are within a certain Levenshtein distance
    of {word}.

    :arg str path: Path taken so far to reach the current node.
    :arg dict node: Current node.
    :arg str word: Query word.
    :arg int distance: Amount of allowed errors.
    :arg cigar: CIGAR string.

    :returns: All words in a trie that have Hamming distance of at most
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
        if char:
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
    def __init__(self: object, words: list=None) -> None:
        """Initialise the class.

        :argwords: List of words.
        """
        self.root = {}

        if words:
            for word in words:
                self.add(word)

    def __contains__(self: object, word: str) -> bool:
        return '' in _find(self.root, word)

    def __iter__(self: object) -> iter:
        return _iterate('', self.root, True)

    def list(self: object, unique: bool=True) -> iter:
        return _iterate('', self.root, unique)

    def add(self: object, word: str, count: int=1) -> None:
        _add(self.root, word, count)

    def get(self: object, word: str) -> dict:
        node = _find(self.root, word)
        if '' in node:
            return node['']
        return None

    def remove(self: object, word: str, count: int=1) -> bool:
        return _remove(self.root, word, count)

    def has_prefix(self: object, word: str) -> bool:
        return _find(self.root, word) != {}

    def fill(self: object, alphabet: tuple, length: int) -> None:
        _fill(self.root, alphabet, length)

    def all_hamming_(self: object, word: str, distance: int) -> iter:
        return map(
            lambda x: (x[0], distance - x[1], x[2]),
            _hamming('', self.root, word, distance, ''))

    def all_hamming(self: object, word: str, distance: int) -> iter:
        return map(
            lambda x: x[0], _hamming('', self.root, word, distance, ''))

    def hamming(self: object, word: str, distance: int) -> str:
        try:
            return next(self.all_hamming(word, distance))
        except StopIteration:
            return None

    def best_hamming(self: object, word: str, distance: int) -> str:
        """Find the best match with {word} in a trie.

        :arg word: Query word.
        :arg distance: Maximum allowed distance.

        :returns: Best match with {word}.
        """
        if self.get(word):
            return word

        for i in range(1, distance + 1):
            result = self.hamming(word, i)
            if result is not None:
                return result

        return None

    def all_levenshtein_(self: object, word: str, distance: int) -> iter:
        return map(
            lambda x: (x[0], distance - x[1], x[2]),
            _levenshtein('', self.root, word, distance, ''))

    def all_levenshtein(self: object, word: str, distance: int) -> iter:
        return map(
            lambda x: x[0], _levenshtein('', self.root, word, distance, ''))

    def levenshtein(self: object, word: str, distance) -> str:
        try:
            return next(self.all_levenshtein(word, distance: int))
        except StopIteration:
            return None

    def best_levenshtein(self: object, word: str, distance: int) -> str:
        """Find the best match with {word} in a trie.

        :arg word: Query word.
        :arg distance: Maximum allowed distance.

        :returns: Best match with {word}.
        """
        if self.get(word):
            return word

        for i in range(1, distance + 1):
            result = self.levenshtein(word, i)
            if result is not None:
                return result

        return None
