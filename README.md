# Trie implementation using nested dictionaries
This library provides a [trie](https://en.wikipedia.org/wiki/Trie)
implementation using nested dictionaries. Apart from the basic operations, a
number of functions for *approximate matching* are implemented.

## Installation
Via [pypi](https://pypi.python.org/pypi/dict-trie):

    pip install dict-trie

From source:

    git clone https://git.lumc.nl/j.f.j.laros/dict-trie.git
    cd dict-trie
    pip install .

## Usage
The library provides the `Trie` class. Full documentation can be found
[here](https://git.lumc.nl/j.f.j.laros/dict-trie)

### Basic operations
Initialisation of the trie is done via the constructor by providing a list of
words.
```python
>>> from dict_trie import Trie
>>>
>>> trie = Trie(['abc', 'te', 'test'])
```

Alternatively, an empty trie can be made to which words can be added with the
`add` function.
```python
>>> trie = Trie()
>>> trie.add('abc')
>>> trie.add('te')
>>> trie.add('test')
```

Membership can be tested with the `in` statement.
```python
>>> 'abc' in trie
True
```

Test whether a prefix is present by using the `has_prefix` function.
```python
>>> trie.has_prefix('ab')
True
```

Remove a word from the trie with the `remove` function. This function returns
`False` if the word was not in the trie.
```python
>>> trie.remove('abc')
True
>>> 'abc' in trie
False
>>> trie.remove('abc')
False
```

Iterate over all words in a trie.
```python
>>> list(trie)
['abc', 'te', 'test']
```

### Approximate matching
A trie can be used to efficiently find a word that is similar to a query word.
This is implemented via a number of functions that search for a word, allowing
a given number of mismatches. These functions are divided in two families, one
using the Hamming distance which only allows substitutions, the other using the
Levenshtein distance which allows substitutions, insertions and deletions.

To find a word that has at most Hamming distance 2 to the word 'abe', the
`hamming` function is used.
```python
>>> trie = Trie(['abc', 'aaa', 'ccc'])
>>> trie.hamming('abe', 2)
'aaa'
```

To get all words that have at most Hamming distance 2 to the word 'abe', the
`all_hamming` function is used. This function returns a generator.
```python
>>> list(trie.all_hamming('abe', 2))
['aaa', 'abc']
```

In order to find a word that is closest to the query word, the `best_hamming`
function is used. In this case a word with distance 1 is returned.
```python
>>> trie.best_hamming('abe', 2)
'abc'
```

The functions `levenshtein`, `all_levenshtein` and `best_levenshtein` are used
in a similar way.

### Other functionalities
A trie can be populated with all words of a fixed length over an alphabet by
using the `fill` function.
```python
>>> trie = Trie()
>>> trie.fill(('a', 'b'), 2)
>>> list(trie)
['aa', 'ab', 'ba', 'bb']
```

The trie data structure can be accessed via the `root` member variable.
```python
>>> trie.root
{'a': {'a': {'': {}}, 'b': {'': {}}}, 'b': {'a': {'': {}}, 'b': {'': {}}}}
>>> trie.root.keys()
['a', 'b']
```
