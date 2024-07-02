import telebot
from telebot import types

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')

@bot.message_handler(commands=['start'])
#Создание кнопок в модели
def start(mess):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Расчет скорости воздуха')
    btn2 = types.KeyboardButton('Площадь воздуховода')
    markup.row(btn1)
    markup.row(btn2)

    bot.send_message(mess.chat.id, 'Привет послушник!', reply_markup=markup)
    bot.register_next_step_handler(mess, test)


@bot.message_handler(commands=['Расчет скорости воздуха'])
def test(message):
    if message.text == 'Расчет скорости воздуха':
        bot.send_message(message.chat.id, 'Введите значение A в метрах')
        a = float(message.float)
        bot.send_message(message.chat.id, 'Введите значение B в метрах')
        b = float(message.float)

        result = a * b
        bot.send_message(message.chat.id, str(result))








bot.polling(non_stop=True)