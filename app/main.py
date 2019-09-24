from aiohttp import web
from app import settings
from app.api.routes import routes


async def _make_app(*args, **kwargs):
    """
    Defines main application `handlers` & `settings`

    :return Application:
    """
    app = web.Application(debug=settings.DEBUG)
    app.router.add_routes(routes)
    return app


def run():
    web.run_app(_make_app(), port=settings.APP_PORT)
