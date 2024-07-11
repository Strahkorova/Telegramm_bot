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
    bot.send_message(mess.chat.id, f'Привет послушник, {mess.from_user.first_name}!', reply_markup= markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "vent-1":
        bot.edit_message_text(f'Необходимо выбрать тип воздуховода:\n Круглый - /round \n Прямоугольный - /rectangle',
            call.message.chat.id, call.message.message_id, parse_mode='html')



@bot.message_handler(commands=['round'])
def callback(message):
    numtwo_a = bot.send_message(message.chat.id, 'Введите диаметр воздуховода в метрах')
    bot.register_next_step_handler(numtwo_a, num2_fun)

def num2_fun(message):
    global D
    D = message.text
    operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
    bot.register_next_step_handler(operu, operi)

def operi(message):
    Class_vent.op(message, D)








@bot.message_handler(commands=['Вентиляция'])
def ventil(message):
    bot.send_message(message.chat.id, 'Выберите функции для расчета в разделе вентиляция', reply_markup=Class_vent.but_ventilation )




























bot.polling(non_stop=True)