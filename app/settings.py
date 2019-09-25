from app.scrapers.bazabet.soccer import BazabetSoccerScrapper
from app.scrapers.parimatch.soccer import SoccerScrapper

APP_PORT = 8085

SECRET = "ABCDEFG!@#$%#"

DEBUG = False

SCHEDULE_URL = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi?n=700"
AJAX_URL = "http://asu.pnu.edu.ua/cgi-bin/timetable.cgi?"

allowed_scrappers = {
    "bazabet": {
        "soccer": BazabetSoccerScrapper
    },
    "parimatch": {
        "soccer": SoccerScrapper
    }
}

TEACHERS_API_CODE = "141"
GROUPS_API_CODE = "142"

BASE_ENCODING = "cp1251"

CONNECTION_TIMEOUT = 1.5
REQUEST_TIMEOUT = 1.5

REDIS_HOST = 'redis'
REDIS_PORT = 6379

CACHE_PERIOD = 60 * 60 * 24
CORS = {
    'Access-Control-Allow-Origin': '*',
}
