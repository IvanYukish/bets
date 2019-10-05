from asyncio import gather
from datetime import datetime
from itertools import chain

from aiohttp import ClientSession

from app.scrapers.base import BaseScrapper


class BazabetBaseScrapper(BaseScrapper):
    url = (
        "https://bookmakersapi.bazabet.com.ua/sportsbook"
        "/rest/public/sportMatches?ln=en"
    )
    detail_url = (
        "https://bookmakersapi.bazabet.com.ua/sportsbook/rest/public/match"
        "/?ln=en&mId={}"
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
    def _get_games_id(raw_data: dict) -> list:
        return [game["id"] for game in chain(*raw_data.values())]

    async def _parse_simple(self, item_id: int,
                            session: ClientSession) -> dict:
        async with session.get(self.detail_url.format(item_id)) as resp:
            return await resp.json()

    async def _parse_all(self, data: dict, session: ClientSession) -> list:
        tasks = []
        for game_id in self._get_games_id(data):
            tasks.append(self._parse_simple(game_id, session))

        return await gather(*tasks)

    @staticmethod
    def _parse_event(event: dict) -> list:
        res = []
        for events in event.values():
            for event in events:
                if "translatableId" in event:
                    continue

                ev = {
                    "type": event["n"],
                    "cof": event["v"]
                }

                if "sbv" in event:
                    ev["sub_value"] = event["sbv"]
                res.append(ev)
        return res

    def _cleared_data(self, parsed_games: list):
        result = []
        for game in parsed_games:
            if "t" in game:
                events = self._parse_event(game["t"])
                if events:
                    result.append(
                        {
                            "name": game["n"],
                            "date": datetime.strptime(
                                game["sd"],
                                "%Y-%m-%dT%H:%M:%S.%f%z"
                            ).timestamp(),
                            "events": events
                        }
                    )
        return result

    async def parse(self) -> list:
        async with ClientSession() as session:
            async with session.get(self._game_type_url) as resp:
                data = await self._parse_all(await resp.json(), session)
                s = self._cleared_data(data)
        return s
