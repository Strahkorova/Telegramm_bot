import telebot
from telebot import types
from Class_vent import calculation
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
    elif call.data == "vent-2":
        num = bot.send_message(call.message.chat.id, 'Укажите расход воздуха в м3/час')
        bot.register_next_step_handler(num, scor_1)
    elif call.data == "vent-3":
        bot.edit_message_text(f'Необходимо выбрать тип воздуховода:\n Круглый - /round_1 \n Прямоугольный - /rectangle_1',
            call.message.chat.id, call.message.message_id, parse_mode='html')

#Расчет площади сечения воздуховода
def scor_1(message):
    global L
    L = message.text
    operu = bot.send_message(message.chat.id, 'Укажите скорость воздуха в м/с')
    bot.register_next_step_handler(operu, scor_2)
def scor_2(message):
    calculation.ploshad(message, L)








#Расчет скорости воздуха в круглом воздуховоде
@bot.message_handler(commands=['round'])
def round_1(message):
    num = bot.send_message(message.chat.id, 'Введите диаметр воздуховода в мм')
    bot.register_next_step_handler(num, round_2)
def round_2(message):
    global D
    D = message.text
    operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
    bot.register_next_step_handler(operu, round_3)
def round_3(message):
    F = (3.14 * (float(D)/1000) ** 2) / 4
    calculation.scorost(message, F)


#Расчет скорости воздуха и расход в прямоугольном воздуховоде
@bot.message_handler(commands=['rectangle', 'rectangle_1'])
def comm(message):
    global com
    com = message.text
    rectangle_1(message)
def rectangle_1(message):
    num = bot.send_message(message.chat.id, 'Введите ширину воздуховода в мм')
    bot.register_next_step_handler(num, rectangle_2)

def rectangle_2(message):
    global A
    A = message.text
    num_2 = bot.send_message(message.chat.id, 'Введите высоту воздуховода в мм')
    bot.register_next_step_handler(num_2, rectangle_3)

def rectangle_3(message):
    global B
    B = message.text
    if com == '/rectangle':
        operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
        bot.register_next_step_handler(operu, rectangle_4)
    elif com == '/rectangle_1':
        operu = bot.send_message(message.chat.id, 'Укажите скорость воздуха в м/с')
        bot.register_next_step_handler(operu, rectangle_4)
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка')

def rectangle_4(message):
    F = (float(A)*float(B))/1000000
    if com == '/rectangle':
        calculation.scorost(message, F)
    elif com == '/rectangle_1':
        calculation.rashod(message, F)













@bot.message_handler(commands=['Вентиляция'])
def ventil(message):
    bot.send_message(message.chat.id, 'Выберите функции для расчета в разделе вентиляция', reply_markup=Class_vent.but_ventilation )




























bot.polling(non_stop=True)