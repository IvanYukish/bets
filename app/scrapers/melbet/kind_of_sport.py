from .settings import kind_of_sports
from .base import MelbetBaseScrapper


def melbet_class_factory() -> dict:
    """create dict of classes for callback since handler"""

    class_table = {}
    for k, v in kind_of_sports.items():
        class_table[k] = type(k, (MelbetBaseScrapper,), {'game_id': k})

    return class_table
