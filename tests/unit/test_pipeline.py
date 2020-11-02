from unittest import mock

import pytest

from pypelines.load import Loader
from pypelines.pipeline import Pipeline
from pypelines.transform import Transformer

DATA = {'key1': 1}


@pytest.fixture
def pipeline():
    return Pipeline(DATA)


@pytest.fixture
def transformer():
    transformer = mock.Mock(spec=Transformer)
    transformer.func = mock.Mock()
    transformer.func.return_value = {'key1': 2}

    return transformer


@pytest.fixture
def loader():
    loader = mock.Mock(spec=Loader)
    loader.load = mock.Mock()

    return loader


def test_when_passing_transformer_then_data_is_transformed(pipeline, transformer):
    result = pipeline | transformer

    assert isinstance(result, Pipeline)
    transformer.func.assert_called_with(DATA)
    assert result.data['key1'] == 2


def test_when_passing_loader_then_data_is_loaded(pipeline, loader):
    result = pipeline | loader

    assert isinstance(result, Pipeline)
    loader.load.assert_called_with(DATA)
