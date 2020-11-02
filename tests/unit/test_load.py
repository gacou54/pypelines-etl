from typing import Dict

import pytest

from pypelines.errors import MissingParameterError
from pypelines.load import Loader


@pytest.fixture
def storage():
    return {'key1': 1}


def make_loader():
    @Loader
    def loader(storage: Dict, data: Dict) -> None:
        storage.update(data)

    return loader


@pytest.mark.parametrize('loader', [make_loader()])
def test_when_calling_without_data_then_args_are_loaded(storage, loader: Loader):
    result = loader(storage)

    assert isinstance(result, Loader)
    assert result.args != ()


@pytest.mark.parametrize('data, loader', [
    ({'key2': 2}, make_loader())
])
def test_when_calling_with_data_then_data_is_loaded(storage, data, loader: Loader):
    result = loader(storage, data=data)

    assert loader.args == ()
    assert loader.kwargs == {}
    assert result is None
    assert 'key2' in storage


@pytest.mark.parametrize('data, loader', [
    ({'key2': 2}, make_loader())
])
def test_when_load_then_data_is_loaded(storage, data, loader: Loader):
    loader(storage).load(data=data)

    assert loader.args != ()
    assert 'key2' in storage


def test_when_making_loader_without_data_parameter_then_raise():
    with pytest.raises(MissingParameterError):
        @Loader
        def a_loader():
            pass
