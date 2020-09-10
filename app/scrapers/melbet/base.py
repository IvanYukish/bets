import asyncio
from asyncio import gather

from aiohttp import ClientSession

import logging
from app.scrapers.base import BaseScrapper
from app.scrapers.melbet.settings import kind_of_sports, change_event_name, lstT

from app.utils import split_list


class MelbetBaseScrapper(BaseScrapper):
    # base_url = 'https://1xbetua.com'
    base_url = 'https://melbet.com'
    base_param = '/LineFeed/GetSportsZip?lng=en&champs=0&partner=8&tf=1000000000&cyberFlag=2'
    tournaments_list = []

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
        print(len(tasks))
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
        tournaments_params = await self.get_tournaments_param(session)
        tournaments_chunk = split_list(tournaments_params, 15)
        tournaments = []
        for tour in tournaments_chunk:
            tournaments.extend(await self.gather_gets(tour, session))

        self.tournaments_list = tournaments

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
        return matches

    async def parse(self):
        async with ClientSession() as session:
            return await self.cleared_match_data(session)

    def get_match_url(self, match_id: int):
        match_by_tournament = {}
        for tournament in self.tournaments_list:
            for match in tournament['Value']['G']:
                if match_by_tournament.get(tournament['Value']['LI']):
                    match_by_tournament[tournament['Value']['LI']].append(match['CI'])
                else:
                    match_by_tournament[tournament['Value']['LI']] = [match['CI']]

        tour_id = self.get_tournament_id_by_match_id(match_id, match_by_tournament)
        match_type = self.tournaments_list[0]["Value"]["SN"].lower().replace(" ", "-")

        return f'https://melbet.com/en/line/{match_type}/{tour_id}/{match_id}/'

    @staticmethod
    def get_tournament_id_by_match_id(val, match_by_tournament):
        for key, values in match_by_tournament.items():
            for value in values:
                if val == value:
                    return key

    async def cleared_match_data(self, session: ClientSession):
        api = []

        for match in await self.get_matches(session):
            try:
                name = self.clear_event_name(f'{match["Value"]["O1"]} || {match["Value"]["O2"]}')
                date = match["Value"]["S"]
                events = match["Value"]["E"]
                api.append({
                    'name': name,
                    'date': date,
                    'url': self.get_match_url(match["Value"]['CI']),
                    'events': self.get_event(events),
                })
            except (TypeError, KeyError):
                logging.warning('match_error')
                # logging.info('match_id = ', match["Value"]["CI"])
        api = sorted(api, key=lambda data: data['date'])
        return api

    @staticmethod
    def clear_event_name(event_name: str):
        new_name = event_name.replace('-', ' ').replace('.', ' ').replace('/', ' ')
        new_name_without_letters = ' '.join([chunk for chunk in new_name.split() if len(chunk) > 1])

        return new_name_without_letters

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
