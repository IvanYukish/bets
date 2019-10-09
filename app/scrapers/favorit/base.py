import json

import requests

from collections import namedtuple

from app.scrapers.base import BaseScrapper
from app.scrapers.favorit.settings import match_id, service_id, method, \
    jsonrpc, lang, type_of_category


class FavoritBaseScrapper(BaseScrapper):
    url = (
        "https://www.favorit.com.ua/en/frontend_api/top/"
    )

    detail_url = (
        "https://www.favorit.com.ua/en/frontend_api/top/{}"
    )
    game_id = None

    async def parse(self) -> list:
        with requests.get(self._game_type_url) as resp:
            data = resp.json()['sports'][0]['events']
            s = self._cleared_data(data)
        return s

    @property
    def _game_type_url(self):
        if not self.game_id:
            print(
                f"[!] Warning: `game_id` don't set. 1 will be used as default"
            )
            self.game_id = 1  # soccer id
        return f"{self.url}{self.game_id}"

    def _cleared_data(self, parsed_games: list) -> list:
        res = []
        api = {
            'bookmaker': 'favorit',
            'game_type': parsed_games[0]["sport_name"],
        }

        for game in parsed_games:
            url = self.generate_url(game)
            match_detail = requests.post(url.base_url, url.url_params).json()
            name = game['event_name']

            api['games'] = {
                'name': name,
                'date': game["event_dt"],
                'events': self._parse_event(match_detail)
            }

            res.append(api['games'])
        return res

    @staticmethod
    def generate_url(game) -> namedtuple:

        event_id = game["participants"][0]["event_id"]
        base_url = "https://www.favorit.com.ua/frontend_api2/"

        url_params = json.dumps({'jsonrpc': jsonrpc, 'method': method,
                                 'params': {'by': {'lang': lang,
                                                   'service_id': service_id,
                                                   'event_id': event_id}},
                                 'id': match_id})

        class_url = namedtuple('url', ['base_url', 'url_params'])
        url = class_url(base_url, url_params)

        return url

    @staticmethod
    def _parse_event(event: dict) -> list:
        event_list = event["result"]
        only_full_time = [event for event in event_list if
                          event["result_type_name"] == 'Full Time']

        cleared_data = [event for event in only_full_time if
                        event['market_name'] in type_of_category]

        item_list = []
        for item in cleared_data:
            for i in range(len(item['outcomes'])):
                item_list.append({
                    'type': item["outcomes"][i]["outcome_short_name"],
                    'cof': item["outcomes"][i]["outcome_coef"]
                })

        return item_list


class StartingSoon(FavoritBaseScrapper):
    url = (
        "https://www.favorit.com.ua/en/frontend_api/starting_soon/"
    )

    async def parse(self) -> list:
        with requests.get(self._game_type_url) as resp:
            data = resp.json()["starting_soon"]
            s = self._cleared_data(data)
        return s

    @property
    def _game_type_url(self):
        return f"{self.url}"
