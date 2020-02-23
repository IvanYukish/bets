import asyncio
from asyncio import gather
from time import time

from aiohttp import ClientSession

import logging
from app.scrapers.base import BaseScrapper
from app.scrapers.melbet.settings import kind_of_sports, change_event_name, lstT


from app.utils import split_list


class MelbetBaseScrapper(BaseScrapper):
    # base_url = 'https://1xbetua.com'
    base_url = 'https://melbet.com'
    base_param = '/LineFeed/GetSportsZip?lng=en&champs=0&partner=8&tf=1000000000&cyberFlag=2'

    game_id = None

    url = (
            base_url + base_param
    )

    async def _get(self, param: str, session: ClientSession):
        async with session.get(self.base_url + param) as response:
            return await response.json()

    async def gather_gets(self, params: list, session: ClientSession):
        tasks = []
        for param in params:
            task = asyncio.ensure_future(self._get(param, session))
            tasks.append(task)
        # print(len(tasks))
        return await gather(*tasks)

    async def get_tournaments_id(self, session: ClientSession):
        if not self.game_id:
            print('[!] Warning: `game_id` don\'t set. soccer will be used as default')
            self.game_id = "rugby"
        response = await self._get(self.base_param, session)
        for i in response['Value']:
            if i['N'] in kind_of_sports.get(self.game_id):
                return [j['LI'] for j in i['L']]

    async def get_tournaments_param(self, session: ClientSession):
        lst_urls = []
        for tournament in await self.get_tournaments_id(session):
            lst_urls.append(f'/LineFeed/GetChampZip?lng=en&champ={tournament}&partner=8&tf=1000000')
        return lst_urls

    async def get_matches_ids(self, session: ClientSession):
        lst_ids = list()
        # tournaments = await self.gather_gets(await self.get_tournaments_param(session), session)
        tournaments_params = await self.get_tournaments_param(session)
        tournaments_chunk = split_list(tournaments_params, 30)
        tournaments = []
        for tour in tournaments_chunk:
            tournaments.extend(await self.gather_gets(tour, session))

        for matches in tournaments:
            for match in matches['Value']['G']:
                lst_ids.append(match['CI'])
        return lst_ids

    async def get_matches_param(self, session: ClientSession):
        matches_url = list()
        matches_id = await self.get_matches_ids(session)
        for match_id in matches_id:
            match_url = f'/LineFeed/GetGameZip?id={match_id}&lng=en&partner=8'
            matches_url.append(match_url)
        return matches_url

    async def get_matches(self, session: ClientSession):
        matches_param = await self.get_matches_param(session)

        matches_chunk = split_list(matches_param, 30)
        matches = []
        for match in matches_chunk:
            matches.extend(await self.gather_gets(match, session))
            # print(time())
        return matches

    async def parse(self):
        async with ClientSession() as session:
            return await self.cleared_data(session)

    async def cleared_data(self, session: ClientSession):
        api = []

        for i, match in enumerate(await self.get_matches(session)):
            try:
                name = f'{match["Value"]["O1"]} - {match["Value"]["O2"]}'
                date = match["Value"]["S"]
                events = match["Value"]["E"]
                api.append({
                    'name': name,
                    'date': date,
                    'events': self.get_event(events),
                })
            except KeyError:
                logging.warning('match_error')
                logging.info('match_id = ', match["Value"]["CI"])
        api = sorted(api, key=lambda data: data['date'])
        return api

    @staticmethod
    def get_markets(event_d: dict):
        t_market = change_event_name['T'].get(event_d["T"])
        if 'P' in event_d:
            return f'{t_market} {event_d["P"]}'
        return t_market

    def get_event(self, events):
        event_data = dict()
        for event in events:
            if (event['G'] in [17]) or event['T'] in lstT:
                market = self.get_markets(event)
                event_data[market] = event["C"]

        return event_data
