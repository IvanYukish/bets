from app.fork_finder.main import find_fork
from app.matcher.settings import DATE_RANGE


class BaseMatcher:
    def __init__(self, scrapper_first_data: dict, scrapper_second_data: dict):
        self.scrapper_first = scrapper_first_data
        self.scrapper_second = scrapper_second_data
        self.data = []

    @classmethod
    async def async_init(cls, scrapper_first, scrapper_second):
        return cls(await scrapper_first.parse(), await scrapper_second.parse())

    def clear_name(self, bets_name: str) -> set:
        return set(bets_name.replace('-', '').lower().split())

    def check_idents_names(self, name_first: set, name_second: set) -> bool:
        return len(name_first.intersection(name_second)) >= 3

    def check_date(self, date_first: int, date_second: int) -> bool:
        return (date_first - date_second) > DATE_RANGE or (date_second - date_first) > DATE_RANGE

    def generate_api(self, melbet_game, favorit_game):
        try:
            api = {"coefficients": {"1": melbet_game['events']['1'], "2": favorit_game['events']['2']}}
            self.data.append(find_fork(api))
            self.data.append(f"{melbet_game['name']}, |||, {favorit_game['name']}")
            self.data.append(melbet_game['url'])
            self.data.append(favorit_game['url'])
        except:
            pass

        try:
            api_next = {"coefficients": {"2": melbet_game['events']['2'], "1": favorit_game['events']['1']}}
            self.data.append(find_fork(api_next))
            self.data.append(f"{melbet_game['name']}, |||, {favorit_game['name']}")
            self.data.append(melbet_game['url'])
            self.data.append(favorit_game['url'])
        except:
            pass

    def find_opposite_match(self):
        for game_1 in self.scrapper_first:
            for game_2 in self.scrapper_second:
                if self.check_idents_names(self.clear_name(game_2['name']), (self.clear_name(game_1['name']))):
                    self.generate_api(game_1, game_2)

        return self.data

    def parse(self):
        return self.find_opposite_match()
