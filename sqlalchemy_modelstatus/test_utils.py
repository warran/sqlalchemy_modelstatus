# -*- encoding: utf-8 -*-

import pytest

from ._utils import *


@pytest.fixture
def nested_list():
    return [
        [1, [2, 3], 4],
        5,
        [6, 7]
    ]


@pytest.fixture
def nested_dict():
    return {
        'key1': 1,
        'key2': [2, 3],
        'key3': {
            'key3_1': 4,
            'key3_2': 5
        },
        'key4': {
            'key4_1': {
                'key4_1_1': [6]
            }
        },
        'key5': {7, 8, 9}
    }


def test_flatten(nested_list):
    assert list(flatten_iterable(nested_list)) == range(1, 8)


def test_nested_values_no_flatten(nested_dict):
    flattened = nested_values(nested_dict, flatten=False)
    for val in flattened:
        assert val in [1, 4, 5, [2, 3], [6], {7, 8, 9}]


def test_nested_values_with_flatten(nested_dict):
    assert set(nested_values(nested_dict)) == set(range(1, 10))
