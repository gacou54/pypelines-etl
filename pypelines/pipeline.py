from typing import Any, Union

from pypelines.load import Loader
from pypelines.transform import Transformer


class Pipeline:

    def __init__(self, data: Any) -> None:
        self.data = data

    def __or__(self, other: Union[Transformer, Loader]) -> 'Pipeline':
        if isinstance(other, Transformer):
            self.data = other.func(self.data)

        elif isinstance(other, Loader):
            other.load(self.data)

        else:
            raise TypeError(f'Accepted types are Transformer, Filter or Loader. Got {type(other)}.')

        return self

    @property
    def value(self):
        return self.data
