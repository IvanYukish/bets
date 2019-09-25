from itertools import chain

import aiohttp

from app.scrapers.base import BaseScrapper


class BazabetBaseScrapper(BaseScrapper):
    url = (
        "https://bookmakersapi.bazabet.com.ua/sportsbook"
        "/rest/public/sportMatches?ln=en"
    )
    game_id = None
    tags = []

    @property
    def _game_type_url(self):
        if not self.game_id:
            print(
                f"[!] Warning: `game_id` don't set. 27 will be used as default"
            )
            self.game_id = 27  # soccer id
        return f"{self.url}&id={self.game_id}"

    @staticmethod
    def _get_cleared_games(raw_data: dict) -> list:
        return [game for game in chain(*raw_data.values()) if "t" in game]

    def filter(self, data: dict) -> list:
        if not self.tags:
            print("[!] Warning: `tags` is empty")
        games = self._get_cleared_games(data)
        result = []
        for game in games:
            coffs = {}
            for cof in chain(*game["t"].values()):
                if not self.tags or cof["n"] in self.tags:
                    coffs[cof["n"]] = cof["v"]
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
            async with session.get(self._game_type_url) as resp:
                data = self.filter(await resp.json())
        return data
