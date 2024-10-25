from typing import Any

response = {
    0: "Запрос выполнен",

    10: "Не допускается смешивание алфавитов в имени.",
    11: "Пароль должен содердать цифры, буквы верхнего и нижнего регистра и символ.",
    12: "Пароли не совпадают.",
    13: "Проверочный код введен не верно.",
    14: "Срок действия проверочного кода истек. Повторите отправку.",
    15: "Номер телефона не соответствует Российскому стандарту.",

    90: "Ошибка на стороне сервера."

}


class ResponseCode(object):
    def __init__(self, code: int, data: Any = None):
        self.code: int = code
        self.answer: str = response[self.code]
        self.data: Any = data

    def __call__(self, *args, **kwargs):
        if self.data is None:
            del self.data
            return {'code': self.code,
                    'answer': self.answer
                    }
        else:
            return {'code': self.code,
                    'answer': self.answer,
                    'data': self.data}
