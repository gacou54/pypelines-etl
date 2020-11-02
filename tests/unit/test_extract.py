import json
from typing import Dict
from unittest import mock

import pytest

from pypelines.extract import Extractor
from pypelines.pipeline import Pipeline


@Extractor
def extractor(json_data: str) -> Dict:
    return json.loads(json_data)


@pytest.fixture
def transformer():
    transformer = mock.Mock()
    transformer.func.return_value = 1

    return transformer


@pytest.mark.parametrize('extractor, expected', [(extractor, 2)])
def test_if_extractor_loads_data(extractor: Extractor, expected):
    result = extractor('{"value": 2}')

    assert isinstance(result, Extractor)
    assert result.data['value'] == expected


@pytest.mark.parametrize('extractor', [extractor])
def test_if_extractor_with_transformer_become_a_pipeline_and_is_init(transformer, extractor: Extractor):
    result = extractor('{"value": 2}') | transformer

    assert isinstance(result, Pipeline)
    assert extractor.data is not None
