from app.scrapers.bazabet.base import BazabetBaseScrapper
from app.scrapers.bazabet.settings import search_coffs


class BazabetTennisScrapper(BazabetBaseScrapper):
    game_id = 29
    tags = search_coffs
