from pprint import pprint

from Classes.HeadHunterAPI import HeadHunterAPI


if __name__ == '__main__':
    hh = HeadHunterAPI()
    vacancies = hh.get_vacancies('python', 1000)
    pprint(vacancies)
