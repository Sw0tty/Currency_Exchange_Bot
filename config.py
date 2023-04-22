"""
Токен бота и возможные валюты
"""
import os


with open(os.path.join(os.getcwd(), 'bot_token', 'token.bin'), 'rb') as file_handler:
    TOKEN = file_handler.read().decode('ascii')


currency_keys = {
    'рубль': ('RUB', '₽'),
    'доллар': ('USD', '$'),
    'евро': ('EUR', '€')
}
