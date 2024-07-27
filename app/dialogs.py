from dataclasses import dataclass
import telebot


but_ventilation = telebot.types.InlineKeyboardMarkup()
but_ventilation.row(telebot.types.InlineKeyboardButton('Скорость воздуха в воздуховоде', callback_data='vent-1'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Площадь воздуховода от скорости', callback_data='vent-2'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Расход воздуха от скорости и сечения', callback_data='vent-3'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Кол-во тепла для нагрева или охлаждения воздуха', callback_data='vent-4'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Ассимиляция тепло - и влагоизбытков', callback_data='vent-5'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Подбор дефлектора типа ЦАГИ', callback_data='vent-6'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Свойства воздуха', callback_data='vent-7'))

but_heat_cool = telebot.types.InlineKeyboardMarkup()
but_heat_cool.row(telebot.types.InlineKeyboardButton('Расход теплоносителя', callback_data='heco-1'))
but_heat_cool.row(telebot.types.InlineKeyboardButton('Скорость теплоносителя от диаметра', callback_data='heco-2'))
but_heat_cool.row(telebot.types.InlineKeyboardButton('Расчет Kvs арматуры', callback_data='heco-3'))


but_holod = telebot.types.InlineKeyboardMarkup()
but_holod.row(telebot.types.InlineKeyboardButton('Коэффициент теплопередачи', callback_data='properties-1'))
but_holod.row(telebot.types.InlineKeyboardButton('Конвертер величин', callback_data='properties-2'))




markup = telebot.types.ReplyKeyboardMarkup()
btn1 = telebot.types.KeyboardButton('/Вентиляция')
btn2 = telebot.types.KeyboardButton('/Тепло-и_Холодоснабжение')
btn3 = telebot.types.KeyboardButton('/Инструменты')
btn4 = telebot.types.KeyboardButton('/stop')
btn5 = telebot.types.KeyboardButton('/DataBase')
markup.row(btn1)
markup.row(btn2, btn3)
markup.row(btn4, btn5)


@dataclass(frozen=True)
class Messages:

    def start(mess):
        if mess.from_user.id == 1125053880:
            return (f'Здравствуйте верховный магистр, {mess.from_user.first_name}! Да прибудет с Вами сила!')
        else:
            return (f'Привет мой юный падаван, {mess.from_user.first_name}! Мудрость от Йоды "Светлая сторона силы путь верный к могуществу инженера!" Да прибудет с тобой сила!')

    def start_djedai(mess):
        return (f'Галактика нуждается в тебе юный джедай! Необходимо добавить к базе научный закон из области естественных наук, например, физики, химии и т.д.'
                f'Ты готов помочь Республике? \n /I_am_ready \n /I_am_not_ready')

    def ventilation(mess):
        return (f'Раздел вентиляция выбрал(а) ты! Верный выбор, путь к верным расчетам! 🖖')

    def thermocooling(mess):
        return (f'Раздел Тепло- и Холодоснабжение выбрал(а) ты! Не используй силу, {mess.from_user.first_name}, используй мозг! 🙂')

    def properties(mess):
        return (f'Раздел инструменты выбрал(а) ты! Страх доступ открывает к тёмной стороне. Страх рождает гнев, гнев рождает ненависть, ненависть — залог страданий ! 🙂')


class Sticers:

    bird = 'CAACAgIAAxkBAAEHDI1mm67IFjG1DGW2hS50y-3sPrTcXQAC_BIAAuvh8Ug4O8mr8lVqtjUE'

    yoda = 'CAACAgQAAxkBAAEHOr5mo-9IUxusoLvm6oTneSo3gadA9gACpAMAAoIVwR3Mn_oILMkK0jUE'

    Nooo = 'CAACAgQAAxkBAAEHOyxmo_qf71_f4ZYrJXYHjN18w2F0UQACAgEAAoIVwR3dIwk_D0OU7DUE'




