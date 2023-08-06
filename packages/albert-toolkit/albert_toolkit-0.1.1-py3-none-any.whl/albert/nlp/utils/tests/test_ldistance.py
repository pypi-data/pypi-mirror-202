import pytest #noqa

from albert.nlp.utils import levenshtein_distance


def test_levenshtein_distance():
    """
    Test that checks to make sure the levenshtein import and rename
    from the main levenshtein lib works as expected
    """
    assert levenshtein_distance(b"", b"") == 0
    assert levenshtein_distance("", "") == 0

    assert levenshtein_distance(b"asdf", b"adf") == 1
    assert levenshtein_distance("ABCD", "AF") == 3
    assert levenshtein_distance("ABCD", "ABCD") == 0
