import json
import requests

from classes import AbstractAPI
from classes import RequestsError


class HeadHunterAPI(AbstractAPI):
    """
    Класс для парсинга вакансий с HeadHunter
    """

    def get_request(self, keyword: str, page: int):
        """
        Метод для получения сырых данных с url https://api.hh.ru/vacancies
        :param keyword: слова для поиска среди вакансий
        :param page: номер страницы с результатами
        :return: список вакансий или исключение RequestsError
        """
        url = 'https://api.hh.ru/vacancies'
        params = {
            'text': keyword,
            'page': page,
            'per_page': 100
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()['items']
        else:
            raise RequestsError('HeadHunter', response.status_code)

    def get_vacancies(self, keyword: str, count: int = 1000):
        """
        Метод для получения списка вакансий со всех доступных страниц
        :param keyword: слова для поиска среди вакансий
        :param count: количество вакансий, которое нужно получить. Не может быть больше 2000
        :return: список вакансий
        """

        if count > 2000:
            return 'Количество вакансий не может превышать 2000'

        pages = count // 100 if count % 100 == 0 else count // 100 + 1
        all_vacancies = []

        for page in range(pages):
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
