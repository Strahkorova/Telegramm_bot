import telebot
from telebot import types

import Class_vent

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')

keybord = telebot.types.InlineKeyboardMarkup()


#keybord.row(  telebot.types.InlineKeyboardButton('Расчет_скорости_воздуха', callback_data='/Расчет_скорости_воздуха'))
keybord.row(  telebot.types.InlineKeyboardButton('Площадь воздуховода', callback_data='no'))




@bot.message_handler(commands=['start'])
#Создание кнопок в модели
def start(mess):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/Расчет_скорости')
    btn2 = types.KeyboardButton('Площадь_воздуховода')
    btn3 = types.KeyboardButton('Площадь_')
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    bot.send_message(mess.chat.id, 'Привет послушник!', reply_markup=keybord)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # Если нажали на одну из 12 кнопок — выводим гороскоп
    if call.data == "no":
        numvan = bot.send_message(call.message.chat.id, 'Введите значение A в метрах')
        bot.register_next_step_handler(numvan, num1_fun)

def num1_fun(message):
    global num1;
    num1 = message.text
    numtwo = bot.send_message(message.chat.id, 'Введите значение B в метрах')
    bot.register_next_step_handler(numtwo, num2_fun)


def num2_fun(message):
    global num2;
    num2 = message.text
    operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
    bot.register_next_step_handler(operu, operi)


def operi(message):
    global oper;
    oper = message.text

    try:
        v = float(num1) / float(num2) / 3600
        bot.send_message(message.chat.id, v)
    except:
        bot.send_message(message.chat.id, "ошибка ведите /start")





@bot.message_handler(commands=['Расчет_скорости'])
def scorost_1(message):
    numvan = bot.send_message(message.chat.id, 'Введите значение A в метрах')
    bot.register_next_step_handler(numvan, num1_fun)

def num1_fun(message):
    global num1;
    num1 = message.text
    numtwo = bot.send_message(message.chat.id, 'Введите значение B в метрах')
    bot.register_next_step_handler(numtwo, num2_fun)


def num2_fun(message):
    global num2;
    num2 = message.text
    operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
    bot.register_next_step_handler(operu, operi)


def operi(message):
    global oper;
    oper = message.text

    try:
        v = float(num1) / float(num2) / 3600
        bot.send_message(message.chat.id, v)
    except:
        bot.send_message(message.chat.id, "ошибка ведите /start")




























bot.polling(non_stop=True)