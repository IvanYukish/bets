from math import ceil

from app import settings
from app.matcher.find_match import BaseMatcher


def split_list(lst: list, chunk_size: int):
    return [lst[i * chunk_size:chunk_size * (i + 1)]
            for i in range(ceil(len(lst) / chunk_size))]


async def get_matcher(bookmaker_first: str, bookmaker_second: str, game_type: str):
    scraper_first = settings.allowed_scrappers[bookmaker_first][game_type]()
    scraper_second = settings.allowed_scrappers[bookmaker_second][game_type]()
    return await BaseMatcher.async_init(scraper_first, scraper_second)