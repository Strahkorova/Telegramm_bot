import telebot
from telebot import types

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')

num1 = -1
num2 = -1


but_ventilation = telebot.types.InlineKeyboardMarkup()

but_ventilation.row(telebot.types.InlineKeyboardButton('Скорость воздуха в сечении', callback_data='vent-1'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Площадь воздуховода от скорости', callback_data='vent-2'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Расход воздуха от скорости и сечения', callback_data='vent-3'))


