from typing import Callable, Any


class Transformer:

    def __init__(self, func: Callable):
        self.func = func

        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)

    def __or__(self, other: 'Transformer') -> 'Transformer':
        return Transformer(
            lambda *args, **kwargs: other.func(self.func(*args, **kwargs))
        )
