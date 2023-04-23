"""
A file with all the handlers for the bot /
Файл со всеми обработчиками для бота
"""
import telebot
from config import TOKEN, currency_keys
from extensions import Converter, request_to_api, UserInputException
from time import strftime, sleep
import logging


logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="a",
                    format="%(asctime)s %(levelname)s %(message)s", encoding="utf8")

today_date = strftime("%Y-%m-%d")

with open('bot_log.log', 'r') as logs:
    check_date = logs.readline()
    if today_date not in check_date:
        with open('bot_log.log', 'a') as logs:
            logs.write(f"------------{today_date}------------\n")


bot = telebot.TeleBot(TOKEN)


def input_com_log(message):
    logging.info(f"""Input command: '{message}'""")


# Each command is painted separately, for clarity and so that each command is in its own handler,
# and not everything is piled up in a heap
@bot.message_handler(commands=['start'])
def start_func(message):
    input_com_log(message.text)
    bot.reply_to(message, f"Здравствуйте! Меня зовут, {bot.user.first_name},"
                          f"и я помогу вам с переводом одной валюты в другую.\n"
                          f"Чтобы ознакомится с моими командами, введите: /help")


@bot.message_handler(commands=['help'])  # To understand each command, read this command
def help_func(message):
    input_com_log(message.text)
    bot.reply_to(message, "У меня есть следующие команды:\n"
                          "\t\t/start - сообщение приветствия\n"
                          "\t\t/values - вывод валют, с которыми я умею работать\n"
                          "\t\t/tutorial - как перевести валюту\n"
                          "\t\t/rates - курсы валют")


@bot.message_handler(commands=['values'])
def values_func(message):
    input_com_log(message.text)
    all_currency = ""
    for i, j in currency_keys.items():
        all_currency += "\t\t•" + j[1] + "•\t" + i + "\n"
    bot.reply_to(message, f"Я умею работать со следующими валютами:\n{all_currency.title()}")


@bot.message_handler(commands=['tutorial'])
def tutorial_func(message):
    input_com_log(message.text)
    bot.reply_to(message, "Для того, чтобы перевести одну валюту в другую, вам нужно написать сообщение типа:\n"
                          "<исходная валюта> <валюта, в которую нужно перевести> <количество исходной валюты>\n"
                          "Например: доллар рубль 20")


@bot.message_handler(commands=['rates'])
def rates_func(message):
    input_com_log(message.text)
    all_currency_rate = ""
    req_text = request_to_api()
    for i, j in currency_keys.items():
        if i == 'доллар':
            continue
        all_currency_rate += "\t\t•" + j[1] + str(req_text['rates'][j[0]]) + "\n"
    bot.reply_to(message, f"Актуальный курс валют:\n{all_currency_rate}")


@bot.message_handler(content_types=['text'])
def reaction_on_text(message: telebot.types.Message):
    if message.text[0] == '/' and len(message.text) > 1 and message.text[1] != ' ':  # Checking the entered command
        logging.info(f"""Incorrect command: '{message.text}'""")
        return bot.reply_to(message, f"Простите, я не знаю такой команды")

    # ---We remove possible commas and change them if the number is not separated by a dot---
    replace_str = ""
    for i, j in enumerate(message.text):
        if j == ',' and message.text[i - 1].isdigit():
            replace_str += '.'
        if j == ',':
            continue
        replace_str += j
    message.text = replace_str
    # ---------------------------------------------------------------------

    values = message.text.lower().split(' ')  # Breakdown and reduction to lowercase

    try:
        if len(values) != 3:  # Считаем параметры
            logging.info(f"""Incorrect parameters: '{message.text}'""")
            raise UserInputException("\t\t• Параметров должно быть 3")
        quote, base, amount = values
        req_currency = Converter.get_price(quote, base, amount)

        # ------Данная проверка меняет окончание при выводе (возможны баги)------
        if quote == 'рубль':
            if amount[-1] in ['2', '3', '4'] and amount[-2::1] not in ['12', '13', '14']:
                quote = quote[:-1] + "я"  # рубля
            elif amount == '1' or len(amount) > 1 and amount[-1] == '1'\
                    and amount[-2] in [str(i) for i in range(2, 10)]:
                pass
            elif amount[-1] in [str(i) for i in range(0, 10)] and amount != '1':
                quote = quote[:-1] + "ей"  # рублей
        elif quote == 'доллар':
            if amount[-1] in ['2', '3', '4'] and amount[-2::1] not in ['12', '13', '14']:
                quote = quote + "а"  # доллара
            elif amount == '1' or len(amount) > 1 and amount[-1] == '1'\
                    and amount[-2] in [str(i) for i in range(2, 10)]:
                pass
            elif amount[-1] in [str(i) for i in range(0, 10)] and amount != '1':
                quote = quote + "ов"  # долларов
        # ------------------------------------------------------------------------

        bot.reply_to(message, f"Переведя {amount} {quote} получим: {currency_keys[base][1]}{req_currency}")
        logging.info(f"Successful Transaction with {values} parameters")

    except Exception as err:
        bot.reply_to(message, f"Причина ошибки:\n{err}")


# This construction catches an exception that is associated with waiting for a response from Telegram servers
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        print(err)
        logging.critical(err)
        sleep(15)
