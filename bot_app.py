"""
Файл со всеми обработчиками для бота
"""
import telebot
from config import TOKEN, currency_keys
from extensions import ConvertException, Converter, request_to_api


bot = telebot.TeleBot(TOKEN)


# Каждая команда расписана отдельно, для наглядности и чтобы каждая команда
# была в своем обработчике, а не свалено все в кучу
@bot.message_handler(commands=['start'])
def start_func(message):
    bot.reply_to(message, f"Здравствуйте! Меня зовут, {bot.user.first_name},"
                          f"и я помогу вам с переведом одной валюты в другую.\n"
                          f"Чтобы ознакомится с моими командами, введите: /help")


@bot.message_handler(commands=['help'])  # Для понимания каждой команды, прочитайте данную команду
def help_func(message):
    bot.reply_to(message, "У меня есть следующие команды:\n"
                          "\t\t/start - сообщение приветствия\n"
                          "\t\t/values - вывод валют, с которыми я умею работать\n"
                          "\t\t/tutorial - как перевести валюту\n"
                          "\t\t/rates - курсы валют")


@bot.message_handler(commands=['values'])
def values_func(message):
    all_currency = ""
    for i, j in currency_keys.items():
        all_currency += "\t\t•" + j[1] + "•\t" + i + "\n"
    bot.reply_to(message, f"Я умею работать со следующими валютами:\n{all_currency.title()}")


@bot.message_handler(commands=['tutorial'])
def tutorial_func(message):
    bot.reply_to(message, "Для того, чтобы перевести одну валюту в другую, вам нужно написать сообщение типа:\n"
                          "<исходная валюта> <валюта, в которую нужно перевести> <количество исходной валюты>\n"
                          "Например: доллар рубль 20")


@bot.message_handler(commands=['rates'])
def rates_func(message):
    all_currency_rate = ""
    req_text = request_to_api()
    for i, j in currency_keys.items():
        if i == 'доллар':
            continue
        all_currency_rate += "\t\t•" + j[1] + str(req_text['rates'][j[0]]) + "\n"
    bot.reply_to(message, f"Актуальный курс валют:\n{all_currency_rate}")


@bot.message_handler(content_types=['text'])
def reaction_on_text(message: telebot.types.Message):
    if message.text[0] == '/' and len(message.text) > 1 and message.text[1] != ' ':  # Проверка введенной команды
        bot.reply_to(message, f"Простите, я не знаю такой команды")
    else:
        while ',' in message.text:  # Если пользователь введет так: quote, base, amount
            message.text = message.text.replace(',', '')

        values = list(map(str.lower, message.text.split(' ')))  # Разбивка и привидение к нижнему регистру
        try:
            if len(values) != 3:  # Считаем параметры
                raise ConvertException("\t\t• Параметров должно быть 3")
        except Exception as e:
            bot.reply_to(message, f"Причина ошибки 1:\n{e}")
        else:
            try:
                quote, base, amount = values
                req_currency = Converter.get_price(quote, base, amount)
                # ------Данная проверка меняет окончание при выводе (возможны баги)------
                if quote == 'рубль':
                    if amount[-1] in ['2', '3', '4'] and amount not in [str(i) for i in range(12, 15)]:
                        quote = quote[:-1] + "я"  # рубля
                    elif len(amount) > 1 and amount[-1] in [str(i) for i in range(1, 21)]\
                            and amount != "1" and amount[-2] == "1":
                        quote = quote[:-1] + "ей"  # рублей
                elif quote == 'доллар':
                    if amount[-1] in ['2', '3', '4'] and amount not in [str(i) for i in range(12, 15)]:
                        quote = quote + "а"  # доллара
                    elif len(amount) > 1 and amount[-1] in [str(i) for i in range(1, 21)]\
                            and amount != "1" and amount[-2] == "1":
                        quote = quote + "ов"  # долларов
                # ------------------------------------------------------------------------
                bot.reply_to(message, f"Переведя {amount} {quote} получим: {currency_keys[base][1]}{req_currency}")
            except Exception as e:
                bot.reply_to(message, f"Причина ошибки 2:\n{e}")  # Вероятно здесь эта ошибка


bot.polling()
