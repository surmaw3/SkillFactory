import telebot
from config import keys, TOKEN
from extensions import ConverionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Отправьте сообщение боту в виде <имя валюты, цену которой он хочет узнать> \
<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.\n' \
           'Увидеть список доступных команд - /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConverionException("Неверное число параметров")

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConverionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f'Цена {amount} {quote} в {base} - {float(total_base) * float(amount)}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)