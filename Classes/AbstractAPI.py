from abc import ABC, abstractmethod


class AbstractAPI(ABC):

    @abstractmethod
    def get_request(self, keyword: str, page: int):
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, count: int):
        pass

    @abstractmethod
    def save_to_json(self, keyword: str, path: str):
        pass
