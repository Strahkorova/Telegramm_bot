import telebot

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')

but_ventilation = telebot.types.InlineKeyboardMarkup()
but_ventilation.row(telebot.types.InlineKeyboardButton('Скорость воздуха в воздуховоде', callback_data='vent-1'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Площадь воздуховода от скорости', callback_data='vent-2'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Расход воздуха от скорости и сечения', callback_data='vent-3'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Кол-во тепла для нагрева или охлаждения воздуха', callback_data='vent-4'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Ассимиляция тепло - и влагоизбытков', callback_data='vent-5'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Расчет дефлектора типа ЦАГИ', callback_data='vent-6'))


but_heat_cool = telebot.types.InlineKeyboardMarkup()



class calculation:

    #Расчет скосроти воздуха в воздуховоде
    def scorost(message, F):
        global L
        L = message.text.replace(',', '.')
        try:
            val = float(L) / (float(F) * 3600)
            bot.send_message(message.chat.id, (f'Скорость в воздуховоде равна - {round(val, 1)} м/с'))
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")

    # Расчет площади воздуховода
    def ploshad_and_CAGI(message, L, cag):
        global v
        v = message.text.replace(',', '.')
        try:
            if cag == 'vent-2':
                F = float(L) / (float(v) * 3600)
                bot.send_message(message.chat.id, (f'Площадь воздуховода равна - {round(F, 5)} м2'))
            elif cag == 'vent-6':
                Do = (0.0188 * ((float(L)/(float(v)))**0.5))*1000
                bot.send_message(message.chat.id, (f'Диаметр подводящего патрубка дефлектора типа ЦАГИ - {round(Do, 0)} мм'))
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")

    #Расчет объекмного расхода воздуха
    def rashod(message, F):
        global v
        v = message.text.replace(',', '.')
        try:
            L = (float(F) * (float(v) * 3600))
            bot.send_message(message.chat.id, (f'Расход воздуха равен - {round(L, 5)} м3/час'))
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")


class assimialtion_thermo_and_cool:

    #Расчет количества теплоты или холода для обработки воздуха
    def thermo_cool(message, L, p, comm):
        global dt
        dt = message.text.replace(',', '.')
        try:
            Q = (float(L) * float(p) * 1.005 * float(dt))/3600
            if comm == '/heat':
                bot.send_message(message.chat.id, (f'Вам {message.from_user.first_name} необходимо - {round(Q, 2)} кВт для нагрева воздуха! 🥵'))
            elif comm == '/cool':
                bot.send_message(message.chat.id, (f'Вам {message.from_user.first_name} необходимо - {round(Q, 2)} кВт для охлаждения воздуха! 🥶'))
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")

    #Расход воздуха на ассимиляцию тепло- и влагоизбытков
    def assimilation(message, Q, t1, p, comm):
        global dt
        dt= message.text.replace(',', '.')
        if comm == '/delete_heat':
            L = (float(Q)*3600)/(float(p)*1.005*(float(dt) - float(t1)))
            bot.send_message(message.chat.id, (f'Вам {message.from_user.first_name} необходимо - {round(L, 2)} м3/час для удавления {Q} кВт теплоты! 🥵'))
        elif comm == '/delete_water':
            L = float(Q)/((float(dt)-float(t1))*float(p))
            bot.send_message(message.chat.id, (f'Вам {message.from_user.first_name} необходимо - {round(L, 2)} м3/час для удавления {Q} г/час влаги! 🐳'))

