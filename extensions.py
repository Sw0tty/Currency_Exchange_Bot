"""
Классы для бота и функция запроса
"""
from config import currency_keys
import requests
import json


class ConvertException(Exception):
    pass


def request_to_api():  # Функция запроса вынесена за класс, так как используется в нескольких командах бота
    data_req = requests.get(
        'https://openexchangerates.org/api/latest.json?app_id=13ef20aae02346669c2c35e1e9ea3cac')
    req_text = json.loads(data_req.content)
    return req_text


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            if quote == base:
                raise ConvertException(f"\t\t• Введены две одинаковые валюты!")
            try:
                inter_quote = currency_keys[quote][0]
            except KeyError:
                raise ConvertException(f"\t\t• Валюта '{quote}' не определена!")
            try:
                inter_base = currency_keys[base][0]
            except KeyError:
                raise ConvertException(f"\t\t• Валюта '{base}' не определена!")
            try:
                amount = float(amount)
                if amount < 0:
                    raise ConvertException("\t\t• Количество должно быть положительным!")
                elif not amount:
                    raise ConvertException("\t\t• Нечего переводить")
            except ValueError:
                raise ConvertException(f"\t\t• Введенное значение '{amount}' не получилось преобразовать в число!")

            req_text = request_to_api()  # Делаем запрос валют

            # ------Выбираем метод перевода------
            if inter_quote == 'RUB':
                result = round(amount / req_text['rates'][inter_quote], 6)
                return result
            else:
                result = round(req_text['rates'][inter_base] * amount, 6)
                return result
            # -----------------------------------
        except Exception as e:
            raise ConvertException(e)
