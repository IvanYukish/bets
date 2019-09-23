from aiohttp.web import get

from app.api.handlers import main_handler

__all__ = ["routes", ]

routes = [
    get(r"/api/{bookmaker}/{game_type}", main_handler),
]
