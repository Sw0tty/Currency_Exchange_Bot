"""
Bot token and possible currencies /
Токен бота и возможные валюты
"""
from os import getenv
from dotenv import load_dotenv


load_dotenv()
TOKEN = getenv('TOKEN')


currency_keys = {
    'рубль': ('RUB', '₽'),
    'доллар': ('USD', '$'),
    'евро': ('EUR', '€')
}
