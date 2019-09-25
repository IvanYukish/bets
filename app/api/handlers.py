import functools
from aiohttp import web
from aiohttp.abc import Request

from app.settings import CORS, allowed_scrappers

__all__ = ["main_handler"]


def cors_headers(f):
    def _add_headers(response):
        for key, value in CORS.items():
            response.headers[key] = value
        return response

    @functools.wraps(f)
    async def new_f(*args):
        response = await f(*args)
        return _add_headers(response)

    return new_f


@cors_headers
async def main_handler(request: Request):
    bookmaker = request.match_info["bookmaker"]
    game_type = request.match_info["game_type"]
    try:
        scrapper = allowed_scrappers[bookmaker][game_type]()
    except KeyError:
        return web.json_response(data={"error": "Not found"}, status=404)
    data = {
        "bookmaker": bookmaker,
        "game_type": game_type,
        "games": await scrapper.parse()
    }
    return web.json_response(data=data, status=200)
