from aiohttp.web import get

from app.api.handlers import main_handler, matcher_handler

__all__ = ["routes", ]

routes = [
    get(r"/api/{bookmaker}/{game_type}", main_handler),
    get(r"/api/matcher/{bookmaker_first}-{bookmaker_second}/{game_type}", matcher_handler),
]
