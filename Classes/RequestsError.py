class RequestsError(Exception):
    def __int__(self, platform, status_code):
        self.platform = platform
        self.status_code = status_code

    def __str__(self):
        return f'Ошибка получения данных с платформы {self.platform}. Код ответа {self.status_code}'
