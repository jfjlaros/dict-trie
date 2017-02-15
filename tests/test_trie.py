"""
Tests for the trie library.
"""
#from __future__ import (
#    absolute_import, division, print_function, unicode_literals)
#from future.builtins import str, zip

from dict_trie import Trie

class TestTrie(object):
    def setup(self):
        self._trie = Trie(['abc', 'abd', 'test', 'te'])

    def test_full_trie(self):
        assert self._trie.root == {
            'a': {
                'b': {
                    'c': {'': {}},
                    'd': {'': {}}}},
            't': {'e': {
                '': {},
                's': {'t': {'': {}}}}}}

    def test_prefix_not_in_trie(self):
        assert 'ab' not in self._trie

    def test_word_in_trie(self):
        assert 'abc' in self._trie

    def test_suffix_not_in_trie(self):
        assert 'abcd' not in self._trie

    def test_word_not_in_trie(self):
        assert 'abe' not in self._trie

    def test_has_prefix(self):
        assert self._trie.has_prefix('ab')

    def test_word_is_prefix(self):
        assert self._trie.has_prefix('abc')

    def test_has_prefix_not(self):
        assert not self._trie.has_prefix('ac')

    def test_has_prefix_not_long(self):
        assert not self._trie.has_prefix('abcd')

    def test_prefix_order(self):
        assert Trie(['test', 'te']).root == Trie(['te', 'test']).root
