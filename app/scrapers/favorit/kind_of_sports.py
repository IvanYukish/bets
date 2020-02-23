from .settings import kinds_of_sport
from .base import FavoritBaseScrapper


def favorit_class_factory() -> dict:
    """create dict of classes for callback since handler"""

    class_table = {}
    for k, v in kinds_of_sport.items():
        class_table[k] = type(k, (FavoritBaseScrapper,), {'game_id': v})

    return class_table
