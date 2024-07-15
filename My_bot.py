import telebot
from telebot import types
from Class_vent import calculation, assimialtion_thermo_and_cool
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
    elif call.data == "vent-4":
        bot.edit_message_text(f'Необходимо выбрать вид обработки воздуховода:\n Нагрев - /heat \n Охлаждение - /cool',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == "vent-5":
        bot.edit_message_text(f'Необходимо выбрать цель ассимиляции:\n Удавление теплоты - /delete_heat \n Удавление влаги - /delete_water',
            call.message.chat.id, call.message.message_id, parse_mode='html')


#Расчет площади сечения воздуховода
def scor_1(message):
    global L
    L = message.text.replace(',', '.')
    operu = bot.send_message(message.chat.id, 'Укажите скорость воздуха в м/с')
    bot.register_next_step_handler(operu, scor_2)
def scor_2(message):
    calculation.ploshad(message, L)

#ассимиляция тепло- и влагоизбытков
@bot.message_handler(commands=['delete_heat', 'delete_water'])
def open(message):
    global comm_assim
    comm_assim = message.text
    if comm_assim == '/delete_heat':
        num = bot.send_message(message.chat.id, 'Укажите количество удаляемой теплоты в кВт')
        bot.register_next_step_handler(num, plotnost_assim)
    elif comm_assim == '/delete_water':
        num = bot.send_message(message.chat.id, 'Укажите количество удаляемой влаги в г/час')
        bot.register_next_step_handler(num, plotnost_assim)

def plotnost_assim(message):
    global Q
    Q = message.text.replace(',', '.')
    plot = bot.send_message(message.chat.id, 'Укажите плотность воздуха в кг/м3')
    bot.register_next_step_handler(plot, delta_first)

def delta_first(message):
    global p
    p = message.text.replace(',', '.')
    if comm_assim == '/delete_heat':
        num = bot.send_message(message.chat.id, 'Укажите температуру приточного воздуха в ºС')
        bot.register_next_step_handler(num, delta_second)
    elif comm_assim == '/delete_water':
        num = bot.send_message(message.chat.id, 'Укажите влагосодержание приточного воздуха г/кг')
        bot.register_next_step_handler(num, delta_second)

def delta_second(message):
    global t1
    t1 = message.text.replace(',', '.')
    if comm_assim == '/delete_heat':
        num = bot.send_message(message.chat.id, 'Укажите температуру удаляемого воздуха в ºС')
        bot.register_next_step_handler(num, rash_assim)
    elif comm_assim == '/delete_water':
        num = bot.send_message(message.chat.id, 'Укажите влагосодержание удаляемого воздуха г/кг')
        bot.register_next_step_handler(num, rash_assim)

def rash_assim(message):
    assimialtion_thermo_and_cool.assimilation(message, Q, t1, p, comm_assim)





#Расчет количества теплоты и холода для обработки воздуха
@bot.message_handler(commands=['heat', 'cool'])
def heat_and_cool(message):
    global heatcool
    heatcool = message.text
    num = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
    bot.register_next_step_handler(num, plotnost)

def plotnost(message):
    global L
    L = message.text.replace(',', '.')
    plot = bot.send_message(message.chat.id, 'Укажите плотность воздуха в кг/м3')
    bot.register_next_step_handler(plot, delta)

def delta(message):
    global p
    p = message.text.replace(',', '.')
    thermo = bot.send_message(message.chat.id, 'Укажите разность температур в К 😊')
    bot.register_next_step_handler(thermo, rash)

def rash(message):
    assimialtion_thermo_and_cool.thermo_cool(message, L, p, heatcool)



#Расчет скорости воздуха и расход в круглом воздуховоде
@bot.message_handler(commands=['round', 'round_1'])
def round_start(message):
    global round_com
    round_com = message.text
    num = bot.send_message(message.chat.id, 'Введите диаметр воздуховода в мм')
    bot.register_next_step_handler(num, round_2)

def round_2(message):
    global D
    D = message.text.replace(',', '.')
    if round_com == '/round':
        operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
        bot.register_next_step_handler(operu, round_3)
    elif round_com == '/round_1':
        operu = bot.send_message(message.chat.id, 'Укажите скорость воздуха в м/с')
        bot.register_next_step_handler(operu, round_3)

def round_3(message):
    F = (3.14 * (float(D)/1000) ** 2) / 4
    if round_com == '/round':
        calculation.scorost(message, F)
    elif round_com == '/round_1':
        calculation.rashod(message, F)





#Расчет скорости воздуха и расход в прямоугольном воздуховоде
@bot.message_handler(commands=['rectangle', 'rectangle_1'])
def rectangle_1(message):
    global rectangle_com
    rectangle_com = message.text
    num = bot.send_message(message.chat.id, 'Введите ширину воздуховода в мм')
    bot.register_next_step_handler(num, rectangle_2)

def rectangle_2(message):
    global A
    A = message.text.replace(',', '.')
    num_2 = bot.send_message(message.chat.id, 'Введите высоту воздуховода в мм')
    bot.register_next_step_handler(num_2, rectangle_3)

def rectangle_3(message):
    global B
    B = message.text.replace(',', '.')
    if rectangle_com == '/rectangle':
        operu = bot.send_message(message.chat.id, 'Укажите расход воздуха в м3/час')
        bot.register_next_step_handler(operu, rectangle_4)
    elif rectangle_com == '/rectangle_1':
        operu = bot.send_message(message.chat.id, 'Укажите скорость воздуха в м/с')
        bot.register_next_step_handler(operu, rectangle_4)
    else:
        bot.send_message(message.chat.id, 'Произошла ошибка')

def rectangle_4(message):
    F = (float(A)*float(B))/1000000
    if rectangle_com == '/rectangle':
        calculation.scorost(message, F)
    elif rectangle_com == '/rectangle_1':
        calculation.rashod(message, F)













@bot.message_handler(commands=['Вентиляция'])
def ventil(message):
    bot.send_message(message.chat.id, 'Выберите функции для расчета в разделе вентиляция', reply_markup=Class_vent.but_ventilation )




























bot.polling(non_stop=True)