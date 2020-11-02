import inspect
from typing import Any, Callable, Dict, Tuple, Optional

from pypelines.errors import MissingParameterError


class Loader:

    def __init__(self, func: Callable) -> None:
        if not _is_data_in_params(func):
            raise MissingParameterError(f'Loader {func.__name__} should have a "data" parameter.')

        self.func = func

        self.args: Tuple = ()
        self.kwargs: Dict = {}

        self.__name__ = func.__name__

    def __call__(self, *args, data=None, **kwargs) -> Optional['Loader']:
        if data is None:
            self.args = args
            self.kwargs = kwargs

            return self

        return self.func(*args, data=data, **kwargs)

    def load(self, data: Any) -> None:
        self.func(*self.args, data=data, **self.kwargs)


def _is_data_in_params(func: Callable) -> bool:
    signature = inspect.signature(func)

    if 'data' in signature.parameters:
        return True

    return False
