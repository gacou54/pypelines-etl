import json
import os

import pandas
import pytest

import pypelines

RESULT_FILEPATH = './tests/integration/data/iris-setosa-mean-petal-length.json'
IRIS_FILEPATH = './tests/integration/data/iris.csv'


@pypelines.Extractor
def extract_csv(iris_filepath: str) -> pandas.DataFrame:
    return pandas.read_csv(iris_filepath)


@pypelines.Extractor
def extract_csv_with_predetermined_path() -> pandas.DataFrame:
    return pandas.read_csv(IRIS_FILEPATH)


@pypelines.Filter
def keep_setosa(df: pandas.DataFrame) -> pandas.DataFrame:
    return df[df['class'] == 'Iris-setosa']


@pypelines.Filter
def keep_petal_length(df: pandas.DataFrame) -> pandas.Series:
    return df['petallength']


@pypelines.Transformer
def mean(series: pandas.Series) -> float:
    return series.mean()


@pypelines.Loader
def write_to_json(output_filepath: str, data: float) -> None:
    with open(output_filepath, 'w') as file:
        json.dump({
            'mean-petal-lenght': {
                'value': data,
                'units': 'cm'
            }
        }, file)


@pypelines.Loader
def write_to_json_with_predetermined_path(data: float) -> None:
    with open(RESULT_FILEPATH, 'w') as file:
        json.dump({
            'mean-petal-lenght': {
                'value': data,
                'units': 'cm'
            }
        }, file)


@pytest.mark.parametrize('extractor, transformer_1, transformer_2, transformer_3, loader', [
    (extract_csv_with_predetermined_path, keep_setosa, keep_petal_length, mean, write_to_json_with_predetermined_path),
    (extract_csv(IRIS_FILEPATH), keep_setosa, keep_petal_length, mean, write_to_json(RESULT_FILEPATH))
])
def test_complete_pipeline(extractor, transformer_1, transformer_2, transformer_3, loader):
    extractor | transformer_1 | transformer_2 | transformer_3 | loader

    with open(RESULT_FILEPATH) as file:
        result = json.load(file)
        assert result == {'mean-petal-lenght': {'value': 1.464, 'units': 'cm'}}

    os.remove(RESULT_FILEPATH)
