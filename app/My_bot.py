from time import sleep
from config import bot
from telebot import types
from Class_vent import calculation, assimialtion_thermo_and_cool, thermo_refrigeration, tools
import dialogs
from dialogs import Messages, Sticers


@bot.message_handler(commands=['start'])
#Создание кнопок в модели
def start(mess):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('/Вентиляция')
    btn2 = types.KeyboardButton('/Тепло-и_Холодоснабжение')
    btn3 = types.KeyboardButton('/Инструменты')
    btn4 = types.KeyboardButton('/stop')
    markup.row(btn1)
    markup.row(btn2, btn3)
    markup.row(btn4)
    bot.send_message(mess.chat.id, Messages.start(mess), reply_markup=markup)
    bot.send_sticker(mess.chat.id, Sticers.bird)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "vent-1":
        bot.edit_message_text(f'Необходимо выбрать тип воздуховода:\n Круглый - /round \n Прямоугольный - /rectangle',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == "vent-2" or call.data == "vent-6":
        global cagi
        cagi = call.data
        num = bot.send_message(call.message.chat.id, 'Укажите расход воздуха в м3/час')
        bot.register_next_step_handler(num, scor_1)
    elif call.data == "vent-3":
        bot.edit_message_text(f'Необходимо выбрать тип воздуховода:\n Круглый - /round_1 \n Прямоугольный - /rectangle_1',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == "vent-4":
        bot.edit_message_text(f'Необходимо выбрать вид обработки воздуховода:\n Нагрев - /heat \n Охлаждение - /cool',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == "vent-5":
        bot.edit_message_text(f'Необходимо выбрать цель ассимиляции:\n Удаление теплоты - /delete_heat \n Удаление влаги - /delete_water',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == 'heco-1':
        bot.edit_message_text(f'Необходимо выбрать тип теплоносителя:\n Вода - /water \n Гликоль - /antifriz',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == 'heco-2':
        bot.edit_message_text(f'Необходимо выбрать тип трубы:\n Пластик PN25 - /plastic \n Сталь - /steel \n Медь - /cuprum',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == 'heco-3':
        num = bot.send_message(call.message.chat.id, 'Укажите расход теплоносителя, в м3/час')
        bot.register_next_step_handler(num, regulation)
    elif call.data == 'properties-1':
        bot.edit_message_text(f'Какие коэффициенты теплоотдачи принять (только для нескольких слоев):'
                              f'\n по рекомендации - /one_layer \n пользовательские - /many_layers',
            call.message.chat.id, call.message.message_id, parse_mode='html')
    elif call.data == 'properties-2':
        bot.edit_message_text(f'Выберите параметр для конвертации:\n Температура - /temperature '
                              f'\n Давление - /pressure \n Кол-во теплоты - /number_heat',
            call.message.chat.id, call.message.message_id, parse_mode='html')


#Расчет значений Kvs для регулирующей арматуры
def regulation(message):
    global Gvs
    Gvs = message.text.replace(',', '.')
    presure = bot.send_message(message.chat.id, 'Укажите потери давления в гидравлической сети, Бар')
    bot.register_next_step_handler(presure, Kvs_system)

def Kvs_system(message):
    global dP
    dP = message.text.replace(',', '.')
    K = (1.1*float(Gvs))/(float(dP)**0.5)
    bot.send_message(message.chat.id, (
        f'Вам {message.from_user.first_name} необходимо - {round(K, 3)} м3/час пропускной способности регулирующего клапана! 😱'))

#Расчет площади сечения воздуховода и размера дефлектора ЦАГИ
def scor_1(message):
    global L
    L = message.text.replace(',', '.')
    if cagi == 'vent-2':
        operu = bot.send_message(message.chat.id, 'Укажите скорость воздуха в м/с')
        bot.register_next_step_handler(operu, scor_2)
    elif cagi == 'vent-6':
        operu = bot.send_message(message.chat.id, 'Укажите скорость воздуха в м/с,'
                                                  'ВАЖНО: принимать равной половине скорости ветра согласно СП "Строительная климатология"!')
        bot.register_next_step_handler(operu, scor_2)

def scor_2(message):
    calculation.ploshad_and_CAGI(message, L, cagi)


########################################################################################################

#Конвертер величин
@bot.message_handler(commands=['temperature', 'pressure', 'number_heat'])
def converter(message):
    global parametr
    parametr = message.text
    if parametr == '/temperature':
        op = bot.send_message(message.chat.id, 'Выберите исходную величину: \n Кельвин - /K \n градус Цельсия ℃ - /C \n '
                                               'градус Фаренгейта ℉ - /F \n градус Ранкина °R - /R', parse_mode='html')
        bot.register_next_step_handler(op, temperature)
    elif parametr == '/number_heat':
        hop = bot.send_message(message.chat.id, 'Выберите исходную величину: \n кВт - /kBt \n Гкал - /Gkall', parse_mode='html')
        bot.register_next_step_handler(hop, number_heat)
    elif parametr == '/pressure':
        op = bot.send_message(message.chat.id, 'Выберите исходную величину: \n кПа - /kPa \n кгс/см2 - /kgs_cm2'
                                               '\n м.вод.ст - /m.water.st \n Бар - /Bar \n мм.рт.ст - /mm.rt.st', parse_mode='html')
        bot.register_next_step_handler(op, pressure)

def temperature(message):
    global param_convert
    param_convert = message.text
    if param_convert == '/K':
        t = bot.send_message(message.chat.id, 'Введите исходную величину в Кельвинах')
        bot.register_next_step_handler(t, start_convert)
    elif param_convert == '/C':
        t = bot.send_message(message.chat.id, 'Введите исходную величину в градусах Цельсия')
        bot.register_next_step_handler(t, start_convert)
    elif param_convert == '/F':
        t = bot.send_message(message.chat.id, 'Введите исходную величину в градусах Фаренгейта')
        bot.register_next_step_handler(t, start_convert)
    elif param_convert == '/R':
        t = bot.send_message(message.chat.id, 'Введите исходную величину в градусах Ранкина')
        bot.register_next_step_handler(t, start_convert)
    elif param_convert == '/stop':
        bot.send_message(message.chat.id, 'Вы прервали выполнение функции')

def number_heat(message):
    global param_convert
    param_convert = message.text
    if param_convert == '/kBt':
        Kv = bot.send_message(message.chat.id, 'Выберите исходную величину в кВт')
        bot.register_next_step_handler(Kv, start_convert)
    elif param_convert == '/Gkall':
        Gk = bot.send_message(message.chat.id, 'Выберите исходную величину в Гкалл')
        bot.register_next_step_handler(Gk, start_convert)
    elif param_convert == '/stop':
        bot.send_message(message.chat.id, 'Вы прервали выполнение функции')

def pressure(message):
    if param_convert == '/kPa':
        kPa = bot.send_message(message.chat.id, 'Выберите исходную величину в кВт')
        bot.register_next_step_handler(kPa, start_convert)
    elif param_convert == '/kgs_cm2':
        kgs_cm2 = bot.send_message(message.chat.id, 'Выберите исходную величину в кгс/см2')
        bot.register_next_step_handler(kgs_cm2, start_convert)
    elif param_convert == '/Bar':
        Bar = bot.send_message(message.chat.id, 'Выберите исходную величину в Бар')
        bot.register_next_step_handler(Bar, start_convert)
    elif param_convert == '/m.water.st':
        m_water_st = bot.send_message(message.chat.id, 'Выберите исходную величину в м.вод.ст')
        bot.register_next_step_handler(m_water_st, start_convert)
    elif param_convert == '/mm.rt.st':
        mm_rt_st = bot.send_message(message.chat.id, 'Выберите исходную величину в мм.рт.ст')
        bot.register_next_step_handler(mm_rt_st, start_convert)
    elif param_convert == '/stop':
        bot.send_message(message.chat.id, 'Вы прервали выполнение функции')

def start_convert(message):
    T = message.text.replace(',', '.')
    if T == '/stop':
        bot.send_message(message.chat.id, 'Вы прервали выполнение функции')
    elif parametr == '/temperature':
        tools.temperature_conv(message, T, param_convert)
    elif parametr == '/pressure':
        tools.pressure_conv(message, T, param_convert)
    elif parametr == '/number_heat':
        tools.heat_conv(message, T, param_convert)



#Расчет коэффициента теплопередачи для однослойной и многослойной стенки
@bot.message_handler(commands=['one_layer', 'many_layers'])
def zero_step(message):
    global layer
    layer = message.text
    one_step(message)

def one_step(message):
    num = bot.send_message(message.chat.id, 'Укажите толщину слоя в мм')
    bot.register_next_step_handler(num, two_step)

def two_step(message):
    global tolshina
    tolshina = message.text.replace(',', '.')
    num = bot.send_message(message.chat.id, 'Укажите коэффициент теплопроводности слоя в Вт/(м²*К)')
    bot.register_next_step_handler(num, three_step)

def three_step(message):
    global teploprovodnost
    teploprovodnost = message.text.replace(',', '.')
    quethion = bot.send_message(message.chat.id, f'Добавить еще слой?:\n Да - /Yes \n Нет - /No', parse_mode='html')
    bot.register_next_step_handler(quethion, four_step)

koeff_thermo = {} #Хранятся толщина и коэффициентр теплопроводности, где толщина это ключ

def four_step(message):
    global yes_no
    yes_no = message.text
    if yes_no == '/No':
        if not koeff_thermo:
            tools.teploperedacha(message, teploprovodnost, tolshina)
        else:
            koeff_thermo[tolshina] = teploprovodnost
            if layer == '/many_layers':
                num = bot.send_message(message.chat.id, 'Укажите коэффициент теплоотдачи для первого вещества в Вт/(м²*К)')
                bot.register_next_step_handler(num, five_step)
            elif layer == '/one_layer':
                tools.koeff_teplo(message, koeff_thermo, 8, 21)
                koeff_thermo.clear()
    elif yes_no == '/Yes':
        koeff_thermo[tolshina] = teploprovodnost
        one_step(message)

def five_step(message):
    global alfa1
    alfa1 = message.text.replace(',', '.')
    num = bot.send_message(message.chat.id, 'Укажите коэффициент теплоотдачи для второго вещества в Вт/(м²*К)')
    bot.register_next_step_handler(num, six_step)

def six_step(message):
    global alfa2
    alfa2 = message.text.replace(',', '.')
    tools.koeff_teplo(message, koeff_thermo, alfa1, alfa2)




#Расчет расхода и скорости теплоносителя в трубе
@bot.message_handler(commands=['water', 'antifriz', 'plastic', 'steel', 'cuprum'])
def open_thermo(message):
    global comm_water
    comm_water = message.text
    if comm_water == '/water' or comm_water == '/antifriz':
        num = bot.send_message(message.chat.id, 'Укажите тепловую нагрузку, переносимую теплоносителем в кВт')
        bot.register_next_step_handler(num, teplo_water)
    else:
        num = bot.send_message(message.chat.id, 'Укажите расход теплоносителя в кг/с')
        bot.register_next_step_handler(num, plotnost_water)

def teplo_water(message):
    global Q
    Q = message.text.replace(',', '.')
    plot = bot.send_message(message.chat.id, 'Укажите разность температур по воде, ℉')
    if comm_water == '/water':
        bot.register_next_step_handler(plot, rashet_rashod_water)
    elif comm_water == '/antifriz':
        bot.register_next_step_handler(plot, teploemkost)

def teploemkost(message):
    global dt
    dt = message.text.replace(',', '.')
    plot = bot.send_message(message.chat.id, 'Укажите удельную теплоемкость гликоля, кДж/(кг*℃)')
    bot.register_next_step_handler(plot, rashet_rashod_water)

def plotnost_water(message):
    global Gw
    Gw = message.text.replace(',', '.')
    plot = bot.send_message(message.chat.id, 'Укажите плотность теплоносителя, кг/м3')
    bot.register_next_step_handler(plot, rashet_rashod_water)

def rashet_rashod_water(message):
    dt = message.text.replace(',', '.')
    if comm_water == '/water' or comm_water == '/antifriz':
        thermo_refrigeration.rashod_teplonositel(message, Q, dt, comm_water)
    else:
        thermo_refrigeration.scorost_teplonositel(message, Gw, comm_water)


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
        num = bot.send_message(message.chat.id, 'Укажите температуру приточного воздуха в ℃')
        bot.register_next_step_handler(num, delta_second)
    elif comm_assim == '/delete_water':
        num = bot.send_message(message.chat.id, 'Укажите влагосодержание приточного воздуха г/кг')
        bot.register_next_step_handler(num, delta_second)

def delta_second(message):
    global t1
    t1 = message.text.replace(',', '.')
    if comm_assim == '/delete_heat':
        num = bot.send_message(message.chat.id, 'Укажите температуру удаляемого воздуха в ℃')
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
    thermo = bot.send_message(message.chat.id, 'Укажите разность температур по воздуху в ℃')
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







################################################################################################


@bot.message_handler(commands=['Вентиляция'])
def ventil(message):
    bot.send_message(message.chat.id, Messages.ventilation(message), reply_markup=dialogs.but_ventilation)

@bot.message_handler(commands=['Тепло-и_Холодоснабжение'])
def thermo_cooling(message):
    bot.send_message(message.chat.id, Messages.thermocooling(message), reply_markup= dialogs.but_heat_cool)

@bot.message_handler(commands=['Инструменты'])
def refrigeration(message):
    bot.send_message(message.chat.id, Messages.properties(message), reply_markup= dialogs.but_holod)













while True:
    try:
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)

