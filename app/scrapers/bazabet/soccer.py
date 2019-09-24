import json
from itertools import chain

import aiohttp

from app.scrapers.base import BaseScrapper
from app.scrapers.bazabet.settings import soccer_url, search_coffs


class BazabetSoccerScrapper(BaseScrapper):
    def _clear_data(self, data: dict) -> list:
        all_games = list(chain(*data.values()))
        result = []
        for game in all_games:
            if "t" in game:
                coffs = []
                for cof in chain(*game["t"].values()):
                    if cof["n"] in search_coffs:
                        coffs.append({cof["n"]: cof["v"]})
                if coffs:
                    result.append(
                        {
                            "name": game["n"],
                            "events": coffs,
                        }
                    )

        return result

    async def parse(self) -> list:
        async with aiohttp.client.ClientSession() as session:
            async with session.get(soccer_url) as resp:
                with open("templ.json", 'w') as f:
                    json.dump(await resp.json(), f)
                data = self._clear_data(await resp.json())
        return data
