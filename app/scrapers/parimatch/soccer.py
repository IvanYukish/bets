import aiohttp
from bs4 import BeautifulSoup
from app.scrapers.base import BaseScrapper
from app.scrapers.parimatch.settings import soccer_url, base_url, sports
from urllib.parse import urlencode


class SoccerScrapper(BaseScrapper):

    @staticmethod
    def _get_sport_ids(body, sport):
        soup = BeautifulSoup(body, 'lxml')
        form_field = soup.find('div', id='lobbySportsHolder')
        data_rows = form_field.find_all('li')[sports[sport]].find('ul',
                                                                  class_="hidden groups").find_all(
            'li')
        if sport == 'football':
            data_rows = data_rows[1:]
        ids = []
        for f in data_rows:
            i = f.find('a').get('hd')
            ids.append(i)
        return ids

    @staticmethod
    def _create_url(ids):
        params = {'hd': ','.join(ids)}
        url = soccer_url + '?' + urlencode(params)
        return url

    @staticmethod
    def _format(all_odds):
        odds = []
        b = False
        for trs in all_odds:
            if b:
                break
            for row in trs:
                try:
                    cells = row.find_all('td')
                except Exception as e:
                    b = True
                    break
                if len(cells) == 17:
                    name = ' - '.join(cells[2].find_all(text=True))
                    events = {
                        "1": ''.join(cells[8].find_all(text=True)).strip(),
                        "X": ''.join(cells[9].find_all(text=True)).strip(),
                        "2": ''.join(cells[10].find_all(text=True)).replace(
                            '\n', '').strip(),
                        "1X": ''.join(cells[11].find_all(text=True)).strip(),
                        "12": ''.join(cells[12].find_all(text=True)).strip(),
                        "X2": ''.join(cells[13].find_all(
                            text=True)).replace('\n', '').strip(),
                    }
                    cleaned_events = {}
                    for key, value in events.items():
                        try:
                            cleaned_events[key] = float(value)
                        except Exception:
                            pass
                    to_add = dict(name=name,
                                  events=cleaned_events)
                    odds.append(to_add)
        return odds

    def _parse(self, body):
        soup = BeautifulSoup(body, 'lxml')
        tables = soup.find('div', id='oddsList').find('form',
                                                      id='f1').find_all('div',
                                                                        class_="container gray")
        trs = [*[t.find_all('tr', class_='bk') for t in tables[1:]]]
        all_odds = self._format(trs)
        return all_odds

    async def _load(self, url):
        async with aiohttp.client.ClientSession() as session:
            async with session.get(url) as resp:
                body = await resp.content.read()
                return body.decode('cp1251')

    async def parse(self):
        resp_body = await self._load(base_url)
        ids = self._get_sport_ids(resp_body, 'football')
        url = self._create_url(ids)
        main_body = await self._load(url)
        result = self._parse(main_body)
        return result
