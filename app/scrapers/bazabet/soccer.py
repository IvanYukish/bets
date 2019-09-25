from app.scrapers.bazabet.base import BazabetBaseScrapper
from app.scrapers.bazabet.settings import search_coffs


class BazabetSoccerScrapper(BazabetBaseScrapper):
    game_id = 27
    tags = search_coffs
