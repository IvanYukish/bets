from app.scrapers.bazabet.soccer import BazabetSoccerScrapper
from app.scrapers.bazabet.tennis import BazabetTennisScrapper
from app.scrapers.parimatch.soccer import SoccerScrapper

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
    }
}

CONNECTION_TIMEOUT = 1.5
REQUEST_TIMEOUT = 1.5

CORS = {
    'Access-Control-Allow-Origin': '*',
}
