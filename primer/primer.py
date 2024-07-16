import telebot
from telebot import types

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')


@bot.message_handler(commands=['start'])
def handle_text(message):
    numvan = bot.send_message(message.chat.id, 'ведите 1 число')
    bot.register_next_step_handler(numvan, num1_fun)


def num1_fun(message):
    global num1;
    num1 = message.text
    numtwo = bot.send_message(message.chat.id, 'ведите 2 число')
    bot.register_next_step_handler(numtwo, num2_fun)


def num2_fun(message):
    global num2;
    num2 = message.text
    operu = bot.send_message(message.chat.id, 'ведите действие')
    bot.register_next_step_handler(operu, operi)


def operi(message):
    global oper;
    oper = message.text
    if oper == "+":
        resylit = int(num1) + int(num2)
        bot.send_message(message.chat.id, resylit)
    elif oper == "-":
        resylit = int(num1) - int(num2)
        bot.send_message(message.chat.id, resylit)
    elif oper == "*":
        resylit = int(num1) * int(num2)
        bot.send_message(message.chat.id, resylit)
    elif oper == "/":
        resylit = int(num1) / int(num2)
        bot.send_message(message.chat.id, resylit)
    else:
        bot.send_message(message.chat.id, "ошибка ведите /start")


bot.polling(none_stop=True)