# Pypelines-ETL

Simple library to make pipelines or ETL

## Installation
```bash
$ pip install pypelines-etl
```

## Usage
`pypelines` allows you to build ETL pipeline. For that, you simply need
the combination of an `Extractor`, some `Transformer` or `Filter`, and a `Loader`.

### Extractor
Making an extractor is fairly easy. Simply decorate a function that return
the data with `Extractor`:
```python
import pandas
from pypelines import Extractor

@Extractor
def read_iris_dataset(filepath: str) -> pandas.Dataframe:
    return pandas.read_csv(filepath)
```

### Transformer or Filter
The `Transformer` and `Filter` decorators are equivalent.

Making a `Transformer` or a `Filter` is even more easy:
```python
import pandas
from pypelines import Filter, Transformer

@Filter
def keep_setosa(df: pandas.DataFrame) -> pandas.DataFrame:
    return df[df['class'] == 'Iris-setosa']


@Filter
def keep_petal_length(df: pandas.DataFrame) -> pandas.Series:
    return df['petallength']


@Transformer
def mean(series: pandas.Series) -> float:
    return series.mean()
```

Note that it is possible to combine the `Transformer` and the `Filter`
to shorten the pipeline syntax. For example:
```python
new_transformer = keep_setosa | keep_petal_length | mean
pipeline = read_iris_dataset('filepath.csv') | new_transformer
print(pipeline.value)
# 1.464
```

### Loader
In order to build a `Loader`, it suffices to decorate a function that takes at
least one `data` parameter. 
```python
import json
from pypelines import Loader

@Loader
def write_to_json(output_filepath: str, data: float) -> None:
    with open(output_filepath, 'w') as file:
        json.dump({'mean-petal-lenght': {'value': data, 'units': 'cm'}}, file)
```
A `Loader` can be called without the `data` parameter,
which loads arguments (like an URL or a path). For example, calling `write_to_json(output.json)`
will not execute the function, but store the `output_filepath` argument until the `Loader` execution in a pipeline.
The standard execution of the function (with the `data` argument) is however still usable `write_to_json(output.json, data=1.464)`.


### ETL pipeline

To make and run the pipeline, simply combine the `Extractor` with the `Transformer`, the `Filter` and the `Loader`
```python
read_iris_dataset('filepath.csv') | keep_setosa | keep_petal_length | mean | write_to_json('output.json')
```
