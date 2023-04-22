"""
Токен бота и возможные валюты
"""
import os
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('TOKEN')


currency_keys = {
    'рубль': ('RUB', '₽'),
    'доллар': ('USD', '$'),
    'евро': ('EUR', '€')
}
