import pytest

from src.trie import Homework, Trie


def make_trie_with_words():
    t = Homework()
    for w in ("apple", "app", "application", "apt", "cat", "cater", "dog"):
        t.insert(w)
    return t


def test_count_words_with_suffix_basic():
    t = make_trie_with_words()
    assert t.count_words_with_suffix("le") == 1
    assert t.count_words_with_suffix("pp") == 1  # app
    assert t.count_words_with_suffix("") == 7  # empty pattern matches all
    assert isinstance(t.count_words_with_suffix("ion"), int)


def test_has_prefix_matches_and_types():
    t = make_trie_with_words()
    assert t.has_prefix("app") is True
    assert t.has_prefix("appl") is True
    assert t.has_prefix("ca") is True
    assert t.has_prefix("z") is False
    assert isinstance(t.has_prefix("a"), bool)


def test_input_validation():
    t = Homework()
    with pytest.raises(TypeError):
        t.count_words_with_suffix(None)  # type: ignore
    with pytest.raises(TypeError):
        t.has_prefix(123)  # type: ignore


def test_interaction_with_base_trie_methods():
    t = make_trie_with_words()
    assert t.contains("app") is True
    assert t.contains("ap") is False
    assert t.starts_with("ap") is True  # path exists
    # has_prefix requires at least one complete word with the prefix
    assert t.has_prefix("ap") is True
