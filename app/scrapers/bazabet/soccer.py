import aiohttp

from app.scrapers.base import BaseScrapper
from app.scrapers.bazabet.settings import soccer_url, basket_url, tennis_url


class SoccerScrapper(BaseScrapper):
    def _clear_data(self, data: dict) -> list:
        result = []
        all_games = []
        for k, v in data.items():
            for match in v:
                if "t" in match:
                    all_games.append(match)
                    events = []
                    some = list(match["t"].values())
                    for s in some:
                        for coff in s:
                            if coff["n"] in ["1", "2", "X", "1X", "X2", "12"]:
                                events.append({coff["n"]: coff["v"]})
                    result.append({
                        "name": match["n"],
                        "events": events
                    })
        return result

    async def parse(self) -> list:
        async with aiohttp.client.ClientSession() as session:
            async with session.get(tennis_url) as resp:
                data = self._clear_data(await resp.json())
        return data
