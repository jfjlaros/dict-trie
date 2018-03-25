"""dict-trie: Basic implementation of a trie.


Copyright (c) 2017 Jeroen F.J. Laros <J.F.J.Laros@lumc.nl>

Licensed under the MIT license, see the LICENSE file.
"""
from .dict_trie import Trie


__version_info__ = ('0', '0', '3')

__version__ = '.'.join(__version_info__)
__author__ = 'Jeroen F.J. Laros'
__contact__ = 'J.F.J.Laros@lumc.nl'
__homepage__ = 'https://github.com/jfjlaros/dict-trie.git'

usage = __doc__.split('\n\n\n')


def doc_split(func):
    return func.__doc__.split('\n\n')[0]


def version(name):
    return '{} version {}\n\nAuthor   : {} <{}>\nHomepage : {}'.format(
        name, __version__, __author__, __contact__, __homepage__)
