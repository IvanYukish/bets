import json

import requests

from app.scrapers.base import BaseScrapper
from app.scrapers.favorit.settings import match_id, service_id, method, \
    jsonrpc, lang, type_of_category


class FavoritBaseScrapper(BaseScrapper):
    url = (
        'https://www.favorit.com.ua/frontend_api2/'
    )

    game_id = None

    async def parse(self) -> list:
        with requests.post(self.url,
                           json=self._generate_params_data_url()) as resp:
            data = resp.json()['result']
            s = self._cleared_data(data)
        return s

    @property
    def _game_type_url(self) -> dict:
        if not self.game_id:
            print(
                '[!] Warning: `game_id` don\'t set. 1 will be used as default'
            )
            self.game_id = 1  # soccer id

        params = {"jsonrpc": "2.0", "method": "frontend/category/get",
                  "params": {
                      "by": {"service_id": 0, "lang": "en",
                             "sport_id": {"$in": [self.game_id]},
                             "tz_diff": 10800}}, "id": 227}

        return params

    def _generate_category_id(self) -> list:
        resp = requests.post(self.url, json=self._game_type_url).json()

        return [elem['category_id'] for elem in resp['result']]

    def _generate_tournament_id(self) -> list:

        params = {"jsonrpc": "2.0", "method": "frontend/event/get",
                  "params": {"by": {"service_id": 0, "lang": "en",
                                    "category_id": None},
                             "count": ["tournament_id"]}, "id": 1099}
        tour_lst = []
        for i, category_id in enumerate(self._generate_category_id()):
            params['params']['by']['category_id'] = category_id
            resp = requests.post(self.url, json=params).json()
            for j in range(len(resp['result'])):
                tour_lst.append(resp['result'][j]['tournament_id'])
        return tour_lst

    def _generate_params_data_url(self) -> dict:

        params = {"jsonrpc": "2.0", "method": "frontend/event/get", "params": {
            "by": {"lang": "en", "service_id": 0,
                   "tournament_id": {"$in": self._generate_tournament_id()},
                   "head_markets": True}},
                  "id": 8021}

        return params

    @staticmethod
    def _generate_params(game) -> dict:

        event_id = game["event_id"]
        url_params = json.dumps({'jsonrpc': jsonrpc, 'method': method,
                                 'params': {'by': {'lang': lang,
                                                   'service_id': service_id,
                                                   'event_id': event_id}},
                                 'id': match_id})

        url = url_params

        return url

    def _cleared_data(self, parsed_games: list) -> list:
        res = []
        api = {
            'bookmaker': 'favorit',
            'game_type': parsed_games[0]["sport_name"],
        }

        for game in parsed_games:
            params = self._generate_params(game)
            match_detail = requests.post(self.url, params).json()
            name = game['event_name']

            api['games'] = {
                'name': name,
                'date': game["event_dt"],
                'events': self._parse_event(match_detail)
            }

            res.append(api['games'])
        return res

    @staticmethod
    def _parse_event(event: dict) -> dict:
        event_list = event["result"]
        only_full_time = [event for event in event_list if
                          event["result_type_name"] == 'Full Time']

        cleared_data = [event for event in only_full_time if
                        event['market_name'] in type_of_category]

        item_list = {}
        for item in cleared_data:
            for i in range(len(item['outcomes'])):
                item_list[
                    item["outcomes"][i]
                    ["outcome_short_name"].replace('(', '').replace(')', '')] \
                    = item["outcomes"][i]["outcome_coef"]

        return item_list
