import telebot



but_ventilation = telebot.types.InlineKeyboardMarkup()
but_ventilation.row(telebot.types.InlineKeyboardButton('Скорость воздуха в сечении', callback_data='vent-1'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Площадь воздуховода от скорости', callback_data='vent-2'))
but_ventilation.row(telebot.types.InlineKeyboardButton('Расход воздуха от скорости и сечения', callback_data='vent-3'))



but_vozd = telebot.types.InlineKeyboardMarkup()
but_vozd.row(telebot.types.InlineKeyboardButton('круглый', callback_data='round'))
but_vozd.row(telebot.types.InlineKeyboardButton('прямоугольный', callback_data='quadro'))
