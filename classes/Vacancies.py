import json

import utils

class Vacancies:
    """
    Класс для представления вакансий. Атрибут класса all - список, который содержит все экземпляры класса
    """
    all = list()

    @staticmethod
    def get_select_json_hh(path) -> list:
        """
        Метод для выбора полей из json файла с результатами парсинга с платформы HeadHunter, неообходимых для инициализации экземпляра класса
        :param path: путь до файла .json с результатами парсинга
        :return: список словарей
        """
        all_select_hh = list()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            for vac in data:
                select_hh = dict()
                select_hh['name'] = vac["name"]
                if vac["salary"]:
                    select_hh['currency'] = utils.get_specific_code(vac["salary"]["currency"])
                    if select_hh['currency'] and select_hh['currency'] != 'RUR':
                        select_hh['salary_min'] = utils.convert_to_rubles(vac["salary"]["from"], select_hh['currency'])
                        select_hh['salary_max'] = utils.convert_to_rubles(vac["salary"]["to"], select_hh['currency'])
                        select_hh['currency'] = 'RUR'
                    else:
                        select_hh['salary_min'] = vac["salary"].get("from")
                        select_hh['salary_max'] = vac["salary"].get("to")
                else:
                    select_hh['salary_min'] = select_hh['salary_max'] = select_hh['currency'] = None
                select_hh['url'] = vac["alternate_url"]
                select_hh['employer'] = vac["employer"]["name"]
                select_hh['platform'] = 'HeadHunter'
                all_select_hh.append(select_hh)
        return all_select_hh

    @staticmethod
    def get_select_json_sj(path) -> list:
        """
        метод для выбора полей из файла .json с результатами парсинга с платформы SuperJob,
        неообходимых для инициализации экземпляра класса
        :param path: путь до файла .json с результатами парсинга
        :return: список словарей
        """
        all_select_sj = list()
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            for vac in data:
                select_sj = dict()
                select_sj['name'] = vac["profession"]
                select_sj['salary_min'] = vac["payment_from"]
                select_sj['salary_max'] = vac["payment_from"]
                select_sj['currency'] = vac["currency"] if vac["currency"] != 'rub' else 'RUR'
                select_sj['url'] = vac["link"]
                select_sj['employer'] = vac["firm_name"]
                select_sj['platform'] = 'SuperJob'
                all_select_sj.append(select_sj)
        return all_select_sj

    @classmethod
    def instantiate_from_json(cls, path_hh, path_sj, is_hh=True, is_sj=True):
        """
        метод инициализации экземпляра класса, данными из файлов .json с результатами парсинга для двух платформ.
        при вызове данного метода, атрибут класса all предварительно очищается
        :param path_hh: путь до файла .json с результатами парсинга с HeadHunter
        :param path_sj: путь до файла .json с результатами парсинга с SuperJob
        :param is_hh: указатель на платформу HH -> True - учитывать данные с платформы / False - не учитывать
        :param is_sj: указатель на платформу SJ -> True - учитывать данные с платформы / False - не учитывать
        :return: None
        """
        cls.all.clear()
        if is_hh:
            for vac_hh in cls.get_select_json_hh(path_hh):
                cls(vac_hh['name'], vac_hh['salary_min'], vac_hh['salary_max'],
                    vac_hh['currency'], vac_hh['url'], vac_hh['employer'], vac_hh['platform'])
        if is_sj:
            for vac_sj in cls.get_select_json_sj(path_sj):
                cls(vac_sj['name'], vac_sj['salary_min'], vac_sj['salary_max'],
                    vac_sj['currency'], vac_sj['url'], vac_sj['employer'], vac_sj['platform'])

    @classmethod
    def sort_by_salary(cls, reverse=True):
        """
        метод сортировки экземпляров класса Vacancies внутри метода all.
        :param reverse: True - сортировка от большей зарплаты к меньшей / False - от меньшей к большей
        :return: атрибут класса all -> list
        """
        cls.all.sort(key=lambda x: x.salary_max if x.salary_max else 0, reverse=reverse)
        cls.all.sort(key=lambda x: x.salary_min if x.salary_min else 0, reverse=reverse)
        return cls.all

    def __init__(self, name, salary_min, salary_max, currency, url, employer, platform):
        self.name = name
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.currency = currency
        self.url = url
        self.employer = employer
        self.platform = platform
        Vacancies.all.append(self)

    def __str__(self):
        str_salary_min = f'от {self.salary_min}' if self.salary_min else ''
        str_salary_max = f'до {self.salary_max}' if self.salary_max else ''
        str_salary = f'{str_salary_min} {str_salary_max} {self.currency}' \
            if self.salary_min or self.salary_max else 'не указана'
        return f'Вакансия с {self.platform}: {self.name} от компании {self.employer}\n{self.url}\nЗарплата {str_salary}'