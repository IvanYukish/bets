from app.scrapers.bazabet.soccer import BazabetSoccerScrapper, \
    BazabetTennisScrapper
from app.scrapers.parimatch.soccer import SoccerScrapper

APP_PORT = 8085

SECRET = "ABCDEFG!@#$%#"

DEBUG = False

SCHEDULE_URL = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi?n=700"
AJAX_URL = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi?"

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

REDIS_HOST = 'redis'
REDIS_PORT = 6379

CACHE_PERIOD = 60 * 60 * 24
CORS = {
    'Access-Control-Allow-Origin': '*',
}
