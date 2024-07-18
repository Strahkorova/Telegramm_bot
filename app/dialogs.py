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
but_heat_cool.row(telebot.types.InlineKeyboardButton('Коэффициент теплопередачи', callback_data='heco-4'))

but_holod = telebot.types.InlineKeyboardMarkup()
but_holod.row(telebot.types.InlineKeyboardButton('Свойства воздуха', callback_data='properties-1'))
but_holod.row(telebot.types.InlineKeyboardButton('Конвертер величин', callback_data='properties-2'))


@dataclass(frozen=True)
class Messages:

    def start(mess):
        return (f'Привет юный падаван, {mess.from_user.first_name}! Мудрость от Йоды "Светлая сторона силы путь верный к могуществу инженера!" Да прибудет с тобой сила!')


    def ventilation(mess):
        return (f'Раздел вентиляция выбрал(а) ты! Верный выбор, путь к верным расчетам! 🖖')

    def thermocooling(mess):
        return (f'Раздел Тепло- и Холодоснабжение выбрал(а) ты! Не используй силу, {mess.from_user.first_name}, используй мозг! 🙂')

    def properties(mess):
        return (f'Раздел инструменты выбрал(а) ты! Страх доступ открывает к тёмной стороне. Страх рождает гнев, гнев рождает ненависть, ненависть — залог страданий ! 🙂')







