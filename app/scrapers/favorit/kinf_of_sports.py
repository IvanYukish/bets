from .settings import kinds_of_sport
from .base import FavoritBaseScrapper, StartingSoon


def class_factory() -> dict:
    """create dict of classes for callback since handler"""

    class_table = {}
    for k, v in kinds_of_sport.items():
        class_table[k] = type(k, (FavoritBaseScrapper,), {'game_id ': v})

    class_table['starting_soon'] = type('starting_soon',
                                        (StartingSoon,), {})

    return class_table
