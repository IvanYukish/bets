from app.scrapers.bazabet.soccer import BazabetSoccerScrapper
from app.scrapers.bazabet.tennis import BazabetTennisScrapper
from app.scrapers.parimatch.soccer import SoccerScrapper
from app.scrapers.favorit.kind_of_sports import favorit_class_factory
from app.scrapers.melbet.kind_of_sport import melbet_class_factory

APP_PORT = 8085

SECRET = "ABCDEFG!@#$%#"

DEBUG = False

allowed_scrappers = {
    "bazabet": {
        "soccer": BazabetSoccerScrapper,
        "tennis": BazabetTennisScrapper,
    },
    "parimatch": {
        "soccer": SoccerScrapper
    },
    "favorit": favorit_class_factory(),
    "melbet": melbet_class_factory(),
}

CONNECTION_TIMEOUT = 1.5
REQUEST_TIMEOUT = 1.5

CORS = {
    'Access-Control-Allow-Origin': '*',
}
