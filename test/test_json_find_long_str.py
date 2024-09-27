import pytest
from utiloori.json import find_long_strings

@pytest.mark.parametrize('input_data, threshold, expected', [
    ({'short': 'abc', 'long': 'abcdefghijk'}, 5, ["['long']"]),
    ({'nested': {'short': 'abc', 'long': 'abcdefghijk'}}, 5, ["['nested']['long']"]),
    (['short', 'abcdefghijk'], 5, ['[1]']),
    ({'list': ['short', 'abcdefghijk']}, 5, ["['list'][1]"]),
    ({'mixed': [{'a': 'short'}, {'b': 'abcdefghijk'}]}, 5, ["['mixed'][1]['b']"]),
    ({}, 5, []),
    ({'all_short': 'abc', 'also_short': 'def'}, 5, []),
    ({'long1': 'abcdefghijk', 'long2': 'lmnopqrstuv'}, 5, ["['long1']", "['long2']"]),
])
def test_find_long_strings(input_data, threshold, expected):
    result = find_long_strings(input_data, threshold)
    assert set(result) == set(expected)

def test_find_long_strings_empty_input():
    assert find_long_strings({}, 5) == []

def test_find_long_strings_no_strings():
    input_data = {'a': 1, 'b': [2, 3], 'c': {'d': 4}}
    assert find_long_strings(input_data, 5) == []

def test_find_long_strings_all_long():
    input_data = {
        'a': 'abcdefghijk',
        'b': ['lmnopqrstuv', 'wxyz123456'],
        'c': {'d': '7890123456'}
    }
    expected = ["['a']", "['b'][0]", "['b'][1]", "['c']['d']"]
    result = find_long_strings(input_data, 5)
    assert set(result) == set(expected)

def test_find_long_strings_mixed_types():
    input_data = {
        'a': 'abcdefghijk',
        'b': 12345,
        'c': ['short', 'longlonglong'],
        'd': {'e': True, 'f': 'alsolonglong'}
    }
    expected = ["['a']", "['c'][1]", "['d']['f']"]
    result = find_long_strings(input_data, 5)
    assert set(result) == set(expected)
