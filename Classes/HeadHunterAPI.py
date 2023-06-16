from urllib.parse import urlencode
import requests

from Classes.AbstractAPI import AbstractAPI


class HeadHunterAPI(AbstractAPI):
    BASE_API_URL = "https://api.hh.ru/"
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }

    def get_vacancies(self, vacancy):
        params = {
            'text': vacancy
        }
        urlencoded_params = urlencode(params)

        request = requests.get(f'{self.__class__.BASE_API_URL}vacancies?{urlencoded_params}', self.__class__.HEADERS)

        return request.json()
