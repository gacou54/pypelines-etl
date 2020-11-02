from typing import Iterable

import numpy
import pytest
from numpy.testing import assert_almost_equal

from pypelines.transform import Transformer


@Transformer
def divide_by_two(value):
    return value / 2


@pytest.mark.parametrize('data, transformer, expected', [
    (4, divide_by_two, 2),
    (4.44, divide_by_two, 2.22),
    (numpy.array([4, 4.44]), divide_by_two, numpy.array([2, 2.22])),
])
def test_if_transformer_is_unaffected_by_decorator(data, transformer, expected):
    result = divide_by_two(data)

    assert_equal(result, expected)


@pytest.mark.parametrize('data, first_transformer, second_transformer, expected', [
    (4, divide_by_two, divide_by_two, 1),
    (4.44, divide_by_two, divide_by_two, 1.11),
    (numpy.array([4, 4.44]), divide_by_two, divide_by_two, numpy.array([1, 1.11])),
])
def test_multiple_transformers(data, first_transformer, second_transformer, expected):
    transformers = first_transformer | second_transformer

    result = transformers(data)

    assert_equal(result, expected)


def assert_equal(value, expected):
    if isinstance(value, Iterable):
        assert_almost_equal(value, expected)
    else:
        assert value == expected
