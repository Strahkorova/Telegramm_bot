import telebot
from telebot import types

bot = telebot.TeleBot('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')
value = ''
old_value = ''
keybord = telebot.types.InlineKeyboardMarkup()

keybord.row(  telebot.types.InlineKeyboardButton(' ', callback_data='no'),
                    telebot.types.InlineKeyboardButton('C', callback_data='C'),
                    telebot.types.InlineKeyboardButton('<=', callback_data='<='),
                    telebot.types.InlineKeyboardButton('/', callback_data='/'))

keybord.row(  telebot.types.InlineKeyboardButton('7', callback_data='7'),
                    telebot.types.InlineKeyboardButton('8', callback_data='8'),
                    telebot.types.InlineKeyboardButton('9', callback_data='9'),
                    telebot.types.InlineKeyboardButton('*', callback_data='*'))

keybord.row(  telebot.types.InlineKeyboardButton('4', callback_data='4'),
                    telebot.types.InlineKeyboardButton('5', callback_data='5'),
                    telebot.types.InlineKeyboardButton('6', callback_data='6'),
                    telebot.types.InlineKeyboardButton('-', callback_data='-'))

keybord.row(  telebot.types.InlineKeyboardButton('1', callback_data='1'),
                    telebot.types.InlineKeyboardButton('2', callback_data='2'),
                    telebot.types.InlineKeyboardButton('3', callback_data='3'),
                    telebot.types.InlineKeyboardButton('+', callback_data='+'))

keybord.row(  telebot.types.InlineKeyboardButton(' ', callback_data=' '),
                    telebot.types.InlineKeyboardButton('0', callback_data='0'),
                    telebot.types.InlineKeyboardButton(',', callback_data=','),
                    telebot.types.InlineKeyboardButton('=', callback_data='='))

@bot.message_handler(commands=['start', 'calc'])
def get_mess(message):
    global value, old_value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keybord)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keybord)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(querry):
    global value, old_value
    data = querry.data

    if data == 'no':
        pass
    elif data == 'C':
        value = ''
    elif data == '=':
        value = str(eval(value))
    else:
        value += data

    if value != old_value:
        if value == '':
            bot.edit_message_text(chat_id=querry.message.chat.id, message_id=querry.message.id, text='0', reply_markup=keybord)
        else:
            bot.edit_message_text(chat_id=querry.message.chat.id, message_id=querry.message.id, text=value,
                                  reply_markup=keybord)
    old_value = value





bot.polling(none_stop=False, interval=0)