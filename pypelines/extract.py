from typing import Callable

from pypelines.pipeline import Pipeline
from pypelines.transform import Transformer


class Extractor:

    def __init__(self, func: Callable) -> None:
        self.func = func
        self.data = None

        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs) -> 'Extractor':
        self.data = self.func(*args, **kwargs)

        return self

    def __or__(self, other: Transformer) -> Pipeline:
        if self.data is None:
            self._init_data()

        result = other.func(self.data)

        return Pipeline(result)

    def _init_data(self) -> None:
        self.data = self.func()
