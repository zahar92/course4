import json
import requests

from Classes.AbstractAPI import AbstractAPI
from Classes.RequestsError import RequestsError


class SuperJobAPI(AbstractAPI):
    """
    Класс для парсинга вакансий с SuperJob
    """

    def get_request(self, keyword: str, page: int):
        """
        Метод для получения сырых данных с url https://api.superjob.ru/2.0/vacancies/
        :param keyword: слова для поиска среди вакансий
        :param page: номер страницы с результатами
        :return: список вакансий или исключение RequestsError
        """
        url = 'https://api.superjob.ru/2.0/vacancies/'
        token = 'v3.r.137621314.4178a5f8e89d58208170cc55d1eb8a827f6e8c76.1a2e8af51379189ed5b443794d49b5de77c4d10f'
        headers = {
            'Host': 'api.superjob.ru',
            'X-Api-App-Id': token,
            'Authorization': 'Bearer r.000000010000001.example.access_token',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'text': keyword,
            'page': page,
            'count': 100
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise RequestsError('HeadHunter', response.status_code)

    def get_vacancies(self, keyword: str, count: int = 5):
        """
        Метод для получения списка вакансий со всех доступных страниц
        :param keyword: слова для поиска среди вакансий
        :param count: количество вакансий, которое нужно получить. Не может быть больше 100
        :return: список вакансий
        """

        all_vacancies = []

        for page in range(count):
            print('Парсинг страницы', page + 1)
            vacancies_per_page = self.get_request(keyword, page)
            if type(vacancies_per_page) is str:
                return vacancies_per_page
            all_vacancies.extend(vacancies_per_page)
        return all_vacancies

    def save_to_json(self, keyword: str, path: str):
        """
        Метод для сохранения вакансий в json файл
        :param keyword: слова для поиска среди вакансий
        :param path: путь сохранения файла
        :return: None
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.get_vacancies(keyword), f, ensure_ascii=False, indent=4)
