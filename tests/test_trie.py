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

    def test_root(self):
        assert self._trie.root == {
            'a': {
                'b': {
                    'c': {'': {}},
                    'd': {'': {}}}},
            't': {'e': {
                '': {},
                's': {'t': {'': {}}}}}}

    def test_word_present(self):
        assert 'abc' in self._trie

    def test_word_absent(self):
        assert 'abx' not in self._trie

    def test_empty_string_present(self):
        assert '' in Trie([''])

    def test_empty_string_absent(self):
        assert '' not in self._trie

    def test_prefix_absent_as_word(self):
        assert 'ab' not in self._trie

    def test_too_long_absent(self):
        assert 'abcd' not in self._trie

    def test_prefix_present(self):
        assert self._trie.has_prefix('ab')

    def test_prefix_absent(self):
        assert not self._trie.has_prefix('ac')

    def test_word_is_prefix(self):
        assert self._trie.has_prefix('abc')

    def test_too_long_prefix_absent(self):
        assert not self._trie.has_prefix('abcd')

    def test_prefix_order(self):
        assert Trie(['test', 'te']).root == Trie(['te', 'test']).root
