import telebot
from telebot import types

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')

@bot.message_handler(commands=['Расчет_скорости'])
def callback(message):
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


