"""
Classes for the bot and the query function /
Классы для бота и функция запроса
"""
from config import currency_keys
import requests
import json
import logging


# Since this exception can be caught before entering the converter, it will be independent
class UserInputException(Exception):
    pass


# But this is the exception to the converter when the message has passed the preliminary check
class ConvertException(Exception):
    pass


# API exception
class RequestsException(ConvertException):
    pass


# The query function is taken out of the class, as it is used in several bot commands
def request_to_api():
    try:
        data_req = requests.get(
            'https://openexchangerates.org/api/latest.json?app_id=13ef20aae02346669c2c35e1e9ea3cac')
        req_text = json.loads(data_req.content)
        return req_text
    except requests.exceptions:  # Ловит ошибки со стороны API
        logging.critical("Request Exception")
        raise RequestsException("Ошибка сервера")


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            logging.info("KeyError")
            raise ConvertException(f"\t\t• Введены две одинаковые валюты!")
        try:
            inter_quote = currency_keys[quote][0]  # Пробуем найти валюту в словаре
        except KeyError:
            logging.error(f"""KeyError: incorrect currency '{quote}'""")
            raise ConvertException(f"\t\t• Валюта '{quote}' не определена!")
        try:
            inter_base = currency_keys[base][0]  # Пробуем найти валюту в словаре
        except KeyError:
            logging.error(f"""KeyError: incorrect currency '{base}'""")
            raise ConvertException(f"\t\t• Валюта '{base}' не определена!")
        try:
            amount = float(amount)
            # Checking our funds for transfer
            if amount < 0:
                logging.info("Negative value input")
                raise ConvertException("\t\t• Количество должно быть положительным!")
            elif not amount:
                logging.info("Zero input")
                raise ConvertException("\t\t• Нечего переводить")
        except ValueError:
            logging.exception(f"""ValueError: '{amount}'""")
            raise ConvertException(f"\t\t• Введенное значение '{amount}' не получилось преобразовать в число!")

        req_text = request_to_api()  # Делаем запрос валют

        # ------Choosing the translation method------
        if inter_quote == 'RUB':
            result = round(amount / req_text['rates'][inter_quote], 6)
            return result
        else:
            result = round(req_text['rates'][inter_base] * amount, 6)
            return result
        # -----------------------------------
