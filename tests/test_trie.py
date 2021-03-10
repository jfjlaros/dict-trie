"""Tests for the trie library."""
from dict_trie import Trie


class TestTrie(object):
    def setup(self: object) -> None:
        self._trie = Trie(['abc', 'abd', 'abd', 'test', 'te'])

    def test_empty(self: object) -> None:
        assert Trie().root == {}

    def test_root(self: object) -> None:
        assert self._trie.root == {
            'a': {
                'b': {
                    'c': {'': 1},
                    'd': {'': 2}}},
            't': {'e': {
                '': 1,
                's': {'t': {'': 1}}}}}

    def test_word_present(self: object) -> None:
        assert 'abc' in self._trie

    def test_word_absent(self: object) -> None:
        assert 'abx' not in self._trie

    def test_empty_string_present(self: object) -> None:
        assert '' in Trie([''])

    def test_empty_string_absent(self: object) -> None:
        assert '' not in self._trie

    def test_prefix_absent_as_word(self: object) -> None:
        assert 'ab' not in self._trie

    def test_too_long_absent(self: object) -> None:
        assert 'abcd' not in self._trie

    def test_prefix_present(self: object) -> None:
        assert self._trie.has_prefix('ab')

    def test_prefix_absent(self: object) -> None:
        assert not self._trie.has_prefix('ac')

    def test_word_is_prefix(self: object) -> None:
        assert self._trie.has_prefix('abc')

    def test_too_long_prefix_absent(self: object) -> None:
        assert not self._trie.has_prefix('abcd')

    def test_prefix_order(self: object) -> None:
        assert Trie(['test', 'te']).root == Trie(['te', 'test']).root

    def test_add(self: object) -> None:
        self._trie.add('abx')
        assert 'abx' in self._trie

    def test_get_present(self: object) -> None:
        assert self._trie.get('abc') == 1

    def test_get_absent(self: object) -> None:
        assert not self._trie.get('abx')

    def test_add_twice(self: object) -> None:
        self._trie.add('abc')
        assert self._trie.get('abc') == 2

    def test_add_multiple(self: object) -> None:
        self._trie.add('abc', 2)
        assert self._trie.get('abc') == 3

    def test_remove_present(self: object) -> None:
        assert self._trie.remove('test')
        assert 'test' not in self._trie
        assert 'te' in self._trie

    def test_remove_prefix_present(self: object) -> None:
        assert self._trie.remove('te')
        assert 'te' not in self._trie
        assert 'test' in self._trie

    def test_remove_absent(self: object) -> None:
        assert not self._trie.remove('xxxx')

    def test_remove_prefix_absent(self: object) -> None:
        assert not self._trie.remove('ab')

    def test_remove_twice(self: object) -> None:
        self._trie.add('abc')
        assert not self._trie.remove('abc')
        assert self._trie.get('abc') == 1
        assert self._trie.remove('abc')
        assert 'abc' not in self._trie

    def test_remove_multile(self: object) -> None:
        self._trie.add('abc', 3)
        assert not self._trie.remove('abc', 2)
        assert self._trie.get('abc') == 2

    def test_remove_force(self: object) -> None:
        self._trie.add('abc')
        assert self._trie.remove('abc', -1)
        assert 'abc' not in self._trie

    def test_iter(self: object) -> None:
        assert set(self._trie) == set(['abc', 'abd', 'te', 'test'])

    def test_list(self: object) -> None:
        assert list(self._trie.list()) == list(self._trie)

    def test_list_non_unique(self: object) -> None:
        assert set(self._trie.list(False)) == set(
            ['abc', 'abd', 'abd', 'te', 'test'])

    def test_fill(self: object) -> None:
        trie = Trie()
        trie.fill(('a', 'b'), 3)
        assert set(trie) == set(
            ['aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb'])

    def test_all_hamming_1_perfect(self: object) -> None:
        assert set(self._trie.all_hamming('abc', 1)) == set(['abc', 'abd'])

    def test_all_hamming_1_not_perfect(self: object) -> None:
        assert set(self._trie.all_hamming('abx', 1)) == set(['abc', 'abd'])

    def test_all_hamming_1_no_match(self: object) -> None:
        assert not list(self._trie.all_hamming('xbx', 1))

    def test_hamming_0_no_prefix(self: object) -> None:
        assert self._trie.hamming('ab', 0) is None

    def test_hamming_0_match(self: object) -> None:
        assert self._trie.hamming('abc', 0) == 'abc'

    def test_hamming_0_match_empty_word(self: object) -> None:
        assert Trie(['']).hamming('', 0) == ''

    def test_hamming_0_match_sub(self: object) -> None:
        assert self._trie.hamming('te', 0) == 'te'

    def test_hamming_0_too_long(self: object) -> None:
        assert self._trie.hamming('abcd', 0) is None

    def test_hamming_1_match(self: object) -> None:
        assert self._trie.hamming('abc', 1) in ['abc', 'abd']

    def test_hamming_1_match_sub(self: object) -> None:
        assert self._trie.hamming('te', 1) == 'te'

    def test_hamming_1_match_1(self: object) -> None:
        assert self._trie.hamming('xbc', 1) == 'abc'

    def test_hamming_1_match_2(self: object) -> None:
        assert self._trie.hamming('axc', 1) == 'abc'

    def test_hamming_1_match_3(self: object) -> None:
        assert self._trie.hamming('abx', 1) in ['abc', 'abd']

    def test_hamming_1_match_4(self: object) -> None:
        assert self._trie.hamming('abd', 1) in ['abc', 'abd']

    def test_hamming_1_no_prefix(self: object) -> None:
        assert self._trie.hamming('ab', 1) is None

    def test_hamming_1_too_long(self: object) -> None:
        assert self._trie.hamming('abcd', 1) is None

    def test_hamming_1_match_sub_1(self: object) -> None:
        assert self._trie.hamming('tx', 1) == 'te'

    def test_hamming_1_match_sub_2(self: object) -> None:
        assert self._trie.hamming('xe', 1) == 'te'

    def test_hamming_1_mismatch(self: object) -> None:
        assert self._trie.hamming('txxt', 1) is None

    def test_hamming_2_match(self: object) -> None:
        assert self._trie.hamming('txxt', 2) == 'test'

    def test_best_hamming_match(self: object) -> None:
        assert self._trie.best_hamming('abd', 1) == 'abd'

    def test_best_hamming_no_match(self: object) -> None:
        assert self._trie.best_hamming('ab', 0) is None

    def test_levenshtein_0_match_empty_word(self: object) -> None:
        assert Trie(['']).levenshtein('', 0) == ''

    def test_levenshtein_0_no_match_empty_word(self: object) -> None:
        assert Trie(['']).levenshtein('a', 0) is None

    def test_levenshtein_1_match_empty_word(self: object) -> None:
        assert Trie(['']).levenshtein('a', 1) == ''

    def test_levenshtein_1_no_match_empty_word(self: object) -> None:
        assert Trie(['']).levenshtein('ab', 1) is None

    def test_all_levenshtein_1_not_perfect(self: object) -> None:
        assert list(self._trie.all_levenshtein('tes', 1)) == ['te', 'test']

    def test_levenshtein_0_match_1(self: object) -> None:
        assert self._trie.levenshtein('abc', 0) in ['abc', 'abd']

    def test_levenshtein_0_match_2(self: object) -> None:
        assert self._trie.levenshtein('te', 0) == 'te'

    def test_levenshtein_1_subst(self: object) -> None:
        assert self._trie.levenshtein('axc', 1) == 'abc'

    def test_levenshtein_1_del(self: object) -> None:
        assert self._trie.levenshtein('ac', 1) == 'abc'

    def test_levenshtein_1_prefix(self: object) -> None:
        assert self._trie.levenshtein('ab', 1) in ['abc', 'abd']

    def test_levenshtein_1_ins(self: object) -> None:
        assert self._trie.levenshtein('abbc', 1) == 'abc'

    def test_all_hamming_2(self: object) -> None:
        assert set(self._trie.all_hamming_('acb', 2)) == set(
            [('abc', 2, '=XX'), ('abd', 2, '=XX')])

    def test_all_levenshtein_2(self: object) -> None:
        assert set(self._trie.all_levenshtein_('acb', 2)) == set([
            ('abc', 2, '=D=I'), ('abd', 2, '=D=I'), ('abc', 2, '=XX'),
            ('abd', 2, '=XX'), ('abc', 2, '=I=D')])

    def test_best_levenshtein_match_emty_word(self: object) -> None:
        assert Trie(['']).best_levenshtein('a', 1) == ''

    def test_best_levenshtein_no_match_emty_word(self: object) -> None:
        assert Trie(['']).best_levenshtein('ab', 1) is None

    def test_best_levenshtein_match(self: object) -> None:
        assert self._trie.best_levenshtein('abd', 1) == 'abd'

    def test_best_levenshtein_no_match(self: object) -> None:
        assert self._trie.best_levenshtein('ab', 0) is None
