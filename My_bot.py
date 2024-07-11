import telebot
from telebot import types

import Class_vent

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')


@bot.message_handler(commands=['start'])
#Создание кнопок в модели
def start(mess):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/Вентиляция')
    btn2 = types.KeyboardButton('/Тепло- и Холодснабжение')
    btn3 = types.KeyboardButton('/Отопление')
    btn3 = types.KeyboardButton('/Холодильная машина')
    btn4 = types.KeyboardButton('/Отмена')
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4)
    bot.send_message(mess.chat.id, 'Привет послушник!', reply_markup= markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "vent-1":
        #bot.send_message(call.message.chat.id, 'Выберите тип воздуховода: /Круглый', reply_markup=Class_vent.but_vozd)
        bot.edit_message_text(
            f'Привет, {call.from_user.first_name}! Вы выбрали <b>Русский</b> 🇷🇺 язык. <b>Продолжить?</b> \n\nIf you want to change your choice, write /car',
            call.message.chat.id, call.message.message_id, parse_mode='html', reply_markup=Class_vent.but_vozd)



@bot.message_handler(commands=['car'])
def callback(message):
    numtwo_a = bot.send_message(message.chat.id, 'Введите диаметр воздуховода в метрах')
    bot.register_next_step_handler(numtwo_a, num2_fun)



def num1_fun(message):
    global num1
    num1 = message.text
    numtwo = bot.send_message(message.chat.id, 'Введите сторону B в метрах')
    bot.register_next_step_handler(numtwo, num2_fun)

def num2_fun(message):
    global num2
    num2 = message.text
    operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
    bot.register_next_step_handler(operu, operi)

def operi(message):
    global oper
    oper = message.text
    try:
        val = float(num1) / float(num2) / 3600
        bot.send_message(message.chat.id, val)
    except:
        bot.send_message(message.chat.id, "ошибка ведите /start")








@bot.message_handler(commands=['Вентиляция'])
def ventil(message):
    bot.send_message(message.chat.id, 'Выберите функции для расчета в разделе вентиляция', reply_markup=Class_vent.but_ventilation )




























bot.polling(non_stop=True)