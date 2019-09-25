from abc import abstractmethod, ABC


class BaseScrapper(ABC):
    @abstractmethod
    def parse(self):
        pass
