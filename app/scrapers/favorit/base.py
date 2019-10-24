import asyncio
import time
from asyncio import gather

from aiohttp import ClientSession

from app.scrapers.base import BaseScrapper
from app.scrapers.favorit.settings import match_id, service_id, method, \
    jsonrpc, lang, type_of_category


class FavoritBaseScrapper(BaseScrapper):
    url = (
        'https://www.favorit.com.ua/frontend_api2/'
    )

    game_id = None

    async def _post(self, params: dict, session: ClientSession):
        async with session.post(self.url, json=params) as response:
            return await response.json(content_type='text')

    async def gather_posts(self, params: list, session: ClientSession):
        tasks = []
        for param in params:
            task = asyncio.ensure_future(self._post(param, session))
            tasks.append(task)
        return await gather(*tasks)

    async def parse(self) -> list:
        async with ClientSession() as session:
            resp = await self.gather_posts(
                await self._generate_params_data_url(session),
                session)
            s = self._cleared_data(resp, session)

            return await s

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

    async def _generate_category_id(self, session: ClientSession) -> list:
        lst_params = []
        resp = await self._post(self._game_type_url, session)
        for elem in resp['result']:
            params = {"jsonrpc": "2.0", "method": "frontend/event/get",
                      "params": {"by": {"service_id": 0, "lang": "en",
                                        "category_id": elem[
                                            'category_id']},
                                 "count": ["tournament_id"]}, "id": 1099}
            lst_params.append(params)
        return lst_params

    async def _generate_tournaments_id(self, session: ClientSession) -> list:

        tour_lst = []
        resp_lst = await self.gather_posts(
            await self._generate_category_id(session), session)

        for resp in resp_lst:
            for j in range(len(resp['result'])):
                tour_lst.append(resp['result'][j]['tournament_id'])
        return tour_lst

    async def _generate_params_data_url(self, session: ClientSession) -> list:
        lst_param = []
        for tour in await self._generate_tournaments_id(session):
            params = {"jsonrpc": "2.0", "method": "frontend/event/get",
                      "params": {
                          "by": {"lang": "en", "service_id": 0,
                                 "tournament_id": {
                                     "$in": [tour]},
                                 "head_markets": True}},
                      "id": 8021}

            lst_param.append(params)
        return lst_param

    @staticmethod
    def _generate_params(game) -> dict:
        event_id = game["event_id"]
        param = {'jsonrpc': jsonrpc, 'method': method,
                 'params': {'by': {'lang': lang,
                                   'service_id': service_id,
                                   'event_id': event_id}},
                 'id': match_id}

        return param

    async def _cleared_data(self, parsed_games: list,
                            session: ClientSession) -> list:
        res = []
        params = []
        api = {
            'bookmaker': 'favorit',
            'game_type': parsed_games[0]['result'][0]["sport_name"],
        }
        for tour in parsed_games:
            for game in tour['result']:
                params.append(self._generate_params(game))

        matches_detail = await self.gather_posts(params, session)

        count = 0
        for tour in parsed_games:
            for game in tour['result']:
                name = game['event_name']

                api['games'] = {
                    'name': name,
                    'date': game['event_dt'],
                    'events': self._parse_event(matches_detail[count])
                }
                count += 1
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
