class BaseScrapper:
    def parse(self):
        pass


class Scrapper(BaseScrapper):
    async def parse(self):
        return {"Some": "cool", "game": "lol"}
