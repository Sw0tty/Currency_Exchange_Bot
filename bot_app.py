"""
Файл со всеми обработчиками для бота
"""
import telebot
from config import TOKEN, currency_keys
from extensions import ConvertException, Converter, request_to_api


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_func(message):
    bot.reply_to(message, f"Здравствуйте! Меня зовут, {bot.user.first_name},"
                          f"и я помогу вам с переведом одной валюты в другую.\n"
                          f"Чтобы ознакомится с моими командами, введите: /help")


@bot.message_handler(commands=['help'])
def help_func(message):
    bot.reply_to(message, "У меня есть следующие команды:\n"
                          "\t\t/start - сообщения приветствия"
                          "\t\t/values - вывод валют, с которыми я умею работать\n"
                          "\t\t/tutorial - как перевести валюту"
                          "\t\t/rates - курсы валют")


@bot.message_handler(commands=['values'])
def values_func(message):
    all_currency = ""
    for i, j in currency_keys.items():
        all_currency += "\t\t•" + j[1] + "•\t" + i + "\n"
    bot.reply_to(message, f"Я умею работать со следующими валютами:\n{all_currency.title()}")


@bot.message_handler(commands=['tutorial'])
def values_func(message):
    bot.reply_to(message, "Для того, чтобы перевести одну валюту в другую, вам нужно написать сообщение типа:"
                          "<исходная валюта> <валюта, в которую нужно перевести> <количество исходной валюты>\n"
                          "Например: доллар рубль 20")


@bot.message_handler(commands=['rates'])
def values_func(message):
    all_currency_rate = ""
    req_text = request_to_api()
    for i, j in currency_keys.items():
        if i == 'доллар':
            continue
        all_currency_rate += "\t\t•" + j[1] + str(req_text['rates'][j[0]]) + "\n"
    bot.reply_to(message, f"Актуальный курс валют:\n {all_currency_rate}")


@bot.message_handler(content_types=['text'])
def function_name(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise ConvertException("\t\t• Аргументов должно быть 3")
    except Exception as e:
        bot.reply_to(message, f"Причина ошибки:\n{e}")
    else:
        try:
            quote, base, amount = values
            req_currency = Converter.get_price(quote, base, amount)

            bot.reply_to(message, f"Переведя {amount} {quote} получим: {currency_keys[base][1]}{req_currency}")
        except Exception as e:
            bot.reply_to(message, f"Причина ошибки:\n{e}")


bot.polling(none_stop=True)
