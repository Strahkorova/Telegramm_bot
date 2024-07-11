import telebot

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')

but_ventilation = telebot.types.InlineKeyboardMarkup()
but_ventilation.row(telebot.types.InlineKeyboardButton('Скорость воздуха в сечении', callback_data='vent-1'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Площадь воздуховода от скорости', callback_data='vent-2'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Расход воздуха от скорости и сечения', callback_data='vent-3'))



def op(message, D):
    global L
    L = message.text
    try:
        F = (3.14 * float(D) ** 2) / 4
        val = float(L) / (float(F) * 3600)
        bot.send_message(message.chat.id, val)
    except:
        bot.send_message(message.chat.id, "ошибка ведите /start")
