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
    id = message.chat.id
    text = message.text
    bot.send_message(id, 'Введите значение A в метрах')
    try:
        a = float(text)
        result = a * 5
        bot.send_message(id, str(result))
    except:
        bot.send_message(id, 'Ошибка ввода')












bot.polling(non_stop=True)