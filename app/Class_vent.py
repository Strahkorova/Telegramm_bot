import prettytable as pt
from config import bot
from database import Database
class calculation:

    #Расчет скосроти воздуха в воздуховоде
    def scorost(message, F):
        global L
        L = message.text.replace(',', '.')
        try:
            val = float(L) / (float(F) * 3600)
            bot.send_message(message.chat.id, (f'Скорость в воздуховоде равна - {round(val, 1)} м/с'))
            Database.select_random(message)
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")

    # Расчет площади воздуховода
    def ploshad_and_CAGI(message, L, cagi):
        global v
        v = message.text.replace(',', '.')
        try:
            if cagi == 'vent-2':
                F = float(L) / (float(v) * 3600)
                bot.send_message(message.chat.id, (f'Площадь воздуховода равна - {round(F, 5)} м2'))
                Database.select_random(message)
            elif cagi == 'vent-6':
                Do = 0.0188 * ((float(L) / (float(v))) ** 0.5) * 1000
                bot.send_message(message.chat.id, (f'Рекомендуемый диаметр дифлектора типа ЦАГИ - {round(Do, 0)} мм'))
                Database.select_random(message)
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")

    #Расчет объекмного расхода воздуха
    def rashod(message, F):
        global v
        v = message.text.replace(',', '.')
        try:
            L = (float(F) * (float(v) * 3600))
            bot.send_message(message.chat.id, (f'Расход воздуха равен - {round(L, 5)} м3/час'))
            Database.select_random(message)
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")

class assimialtion_thermo_and_cool:

    #Расчет количества теплоты или холода для обработки воздуха
    def thermo_cool(message, L, p, comm):
        global dt
        dt = message.text.replace(',', '.')
        try:
            Q = (float(L) * float(p) * 1.005 * float(dt)) / 3600
            if comm == '/heat':
                bot.send_message(message.chat.id, (
                    f'Вам {message.from_user.first_name} необходимо - {round(Q, 2)} кВт для нагрева воздуха! 🥵'))
                Database.select_random(message)
            elif comm == '/cool':
                bot.send_message(message.chat.id, (
                    f'Вам {message.from_user.first_name} необходимо - {round(Q, 2)} кВт для охлаждения воздуха! 🥶'))
                Database.select_random(message)
        except:
            bot.send_message(message.chat.id, "ошибка ведите /start")

    #Расход воздуха на ассимиляцию тепло- и влагоизбытков
    def assimilation(message, Q, t1, p, comm):
        global dt
        dt = message.text.replace(',', '.')
        if comm == '/delete_heat':
            L = (float(Q) * 3600) / (float(p) * 1.005 * (float(dt) - float(t1)))
            bot.send_message(message.chat.id, (
                f'Вам {message.from_user.first_name} необходимо - {round(L, 2)} м3/час для удавления {Q} кВт теплоты! 🥵'))
            Database.select_random(message)
        elif comm == '/delete_water':
            L = float(Q) / ((float(dt) - float(t1)) * float(p))
            bot.send_message(message.chat.id, (
                f'Вам {message.from_user.first_name} необходимо - {round(L, 2)} м3/час для удавления {Q} г/час влаги! 🐳'))
            Database.select_random(message)

class thermo_refrigeration:

    #Определение расхода теплоносителя
    def rashod_teplonositel(message, Q, dt, name):
        if name == '/water':
            G = float(Q) / (4.18 * float(dt))
            bot.send_message(message.chat.id, (f'Массовый расход воды в системе равен - {round(G, 3)} кг/с'))
            Database.select_random(message)
        elif name == '/antifriz':
            cp = message.text.replace(',', '.')
            G = float(Q) / (float(cp) * float(dt))
            bot.send_message(message.chat.id, (f'Массовый расход антифриз в системе равен - {round(G, 3)} кг/с'))
            Database.select_random(message)

    def scorost_teplonositel(message, G, type_tube):
        pw = message.text.replace(',', '.')

        plastic = {'20x3,4': 0.0001367, '25x4,2': 0.0002164, '32x5,4': 0.0003529, '40x6,7': 0.0005557,
                   '50x8,3': 0.0008761, '63x10,5': 0.001385, '75x12,5': 0.001963, '90x15': 0.002827}

        steel = {'20x2,8': 0.0001627, '25x2,8': 0.0002954, '32x2,8': 0.0005471, '40x3,0': 0.0009074,
                 '57x3,5': 0.001962, '76x3,5': 0.003737, '89x3,5': 0.005278, '108x4,0': 0.00785,
                 '133x4,5': 0.01207, '159x5,0': 0.01742, '219x6,0': 0.03428}

        cuprum = {'8x1,0': 0.00002826, '10x1,0': 0.00005024, '11x1,5': 0.00005024, '12x2,0': 0.00005024,
                  '13x1,5': 0.0000785, '13x2,0': 0.00006358, '26x2,0': 0.0003799, '45x3,0': 0.001194, '50x3,0': 0.001519}

        if type_tube == '/plastic':
            thermo_refrigeration.tube_scorost(message, G, pw, plastic)
        elif type_tube == '/steel':
            thermo_refrigeration.tube_scorost(message, G, pw, steel)
        elif type_tube == '/cuprum':
            thermo_refrigeration.tube_scorost(message, G, pw, cuprum)

    def tube_scorost(message, G, pw, dicty):
        data = []
        for tube, place in dicty.items():
            v = float(G) / (float(pw) * place)
            tube_scor = (tube, place, v)
            data.append(tube_scor)

        table = pt.PrettyTable(['Труба, мм', 'Живое сечение, м2', 'Скорость, м/с'])
        for tube, place, speed in data:
            table.add_row([tube, f'{place:.5f}', f'{speed:.3f}'])
        bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode='html')
        Database.select_random(message)

class tools:

    def teploperedacha(message, tolshina, teploprov):
        k = 1/((1/8)+(float(tolshina)/1000) / float(teploprov)+(1/21))
        bot.send_message(message.chat.id, f'Коэффициент теплопередачи однослойной ограждающей стенки равен - {round(k, 3)} Вт/(м2*К)')
        Database.select_random(message)

    def koeff_teplo(message, dicty, a1, a2):
        data = []
        list_R = []
        n = 1
        for tolshina, teploprov in dicty.items():

            R = (float(tolshina)/1000) / float(teploprov)
            k_scor = (n, float(tolshina), float(teploprov), R)
            data.append(k_scor)
            list_R.append(R)
            n +=1

        SR = sum(list_R)
        k = 1/((1/float(a1))+SR+(1/float(a2)))

        table = pt.PrettyTable(['Слой', 'Толщина, мм', 'ʎ, Вт/(м2*К)', 'R, Вт/(м2*К)'])
        for n, b, v, r in data:
           table.add_row([n, f'{b:.1f}', f'{v:.3f}', f'{r:.2f}'])
        bot.send_message(message.chat.id, f'<pre>{table}</pre>', parse_mode='html')
        bot.send_message(message.chat.id, f'Коэффициент теплопередачи многослойной ограждающей стенки равен - {round(k, 3)} Вт/(м2*К)')
        Database.select_random(message)

    def temperature_conv(message, T, param):
        if param == '/K':
            C = float(T)-273.15
            F = float(T)*1.8-459.67
            R = float(T)*1.8
            bot.send_message(message.chat.id, f'Кельвин: {T} K \n градус Цельсия: {C: .3f} ℃ \n '
                                              f'градус Фаренгейта: {F: .3f} ℉ \n градус Ранкина: {R: .3f} °R', parse_mode='html')
            Database.select_random(message)

        elif param == '/C':
            K = float(T)+273.15
            F = float(T)*1.8+32
            R = (float(T)+273.15)*1.8
            bot.send_message(message.chat.id,
                             f'Кельвин: {K: .3f} K \n градус Цельсия: {T} ℃ \n '
                             f'градус Фаренгейта: {F: .3f} ℉ \n градус Ранкина: {R: .3f} °R', parse_mode='html')
            Database.select_random(message)

        elif param == '/F':
            K = (float(T)+459.67)*(5/9)
            C = (float(T)-32)*(5/9)
            R = float(T)+459.67
            bot.send_message(message.chat.id,
                             f'Кельвин: {K: .3f} K \n градус Цельсия: {C: .3f} ℃ \n '
                             f'градус Фаренгейта: {T} ℉ \n градус Ранкина: {R: .3f} °R', parse_mode='html')
            Database.select_random(message)

        elif param == '/R':
            K = float(T)/1.8
            C = (float(T)/1.8)-273.15
            F = float(T) - 459.67
            bot.send_message(message.chat.id,
                             f'Кельвин: {K: .3f} K \n градус Цельсия: {C: .3f} ℃ \n '
                             f'градус Фаренгейта: {F: .3f} ℉ \n градус Ранкина: {T} °R', parse_mode='html')
            Database.select_random(message)

    def pressure_conv(message, T, param):
        P = float(T)
        if param == '/kPa':
            kgs_cm2 = P*0.0102
            Bar = P/100
            m_water_st = P*0.10197
            mm_rt_st = P*7.5006
            bot.send_message(message.chat.id, f' кПа: {T} \n кгс/см2: {kgs_cm2: .3f} \n Бар: {Bar: .3f}'
                                              f' \n м.вод.ст: {m_water_st: .3f} \n мм.рт.ст: {mm_rt_st: .3f}', parse_mode='html')
            Database.select_random(message)

        elif param == '/kgs_cm2':
            kPa = (P/1.0197)*100
            Bar = P/1.0197
            m_water_st = P*10
            mm_rt_st = P*735.56
            bot.send_message(message.chat.id, f' кПа: {kPa: .3f} \n кгс/см2: {T} \n Бар: {Bar: .3f}'
                                              f' \n м.вод.ст: {m_water_st: .3f} \n мм.рт.ст: {mm_rt_st: .3f}', parse_mode='html')
            Database.select_random(message)

        elif param == '/Bar':
            kgs_cm2 = P*1.0197
            kPa = P*100
            m_water_st = P*10.197
            mm_rt_st = P*750.06
            bot.send_message(message.chat.id, f' кПа: {kPa: .3f} \n кгс/см2: {kgs_cm2: .3f} \n Бар: {T}'
                                              f' \n м.вод.ст: {m_water_st: .3f} \n мм.рт.ст: {mm_rt_st: .3f}', parse_mode='html')
            Database.select_random(message)

        elif param == '/m_water_st':
            kgs_cm2 = P/10
            Bar = P/10.197
            kPa = P/0.10197
            mm_rt_st = P*73.55
            bot.send_message(message.chat.id, f' кПа: {kPa: .3f} \n кгс/см2: {kgs_cm2: .3f} \n Бар: {Bar: .3f}'
                                              f' \n м.вод.ст: {T} \n мм.рт.ст: {mm_rt_st: .3f}', parse_mode='html')
            Database.select_random(message)

        elif param == '/mm_rt_st':
            kgs_cm2 = P/735.56
            Bar = P/750.06
            m_water_st = P/73.556
            kPa = P/7.5006
            bot.send_message(message.chat.id, f' кПа: {kPa: .3f} \n кгс/см2: {kgs_cm2: .3f} \n Бар: {Bar: .3f}'
                                              f' \n м.вод.ст: {m_water_st: .3f} \nмм.рт.ст: {T}', parse_mode='html')
            Database.select_random(message)

    def heat_conv(message, T, param):
        if param == '/kBt':
            G = float(T)/1163
            bot.send_message(message.chat.id, f'кВт: {T} \n Гкал: {G: .4f}', parse_mode='html')
            Database.select_random(message)
        elif param == '/Gkall':
            K = float(T) * 1163
            bot.send_message(message.chat.id, f'кВт: {K: .3f} \n Гкал: {T}', parse_mode='html')
            Database.select_random(message)
