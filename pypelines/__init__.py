from .extract import Extractor
from .load import Loader
from .pipeline import Pipeline
from .transform import Transformer

Filter = Transformer

__all__ = [
    'Extractor',
    'Filter',
    'Loader',
    'Pipeline',
    'Transformer',
]
