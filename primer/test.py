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










@bot.callback_query_handler(func=lambda callback: True)
def language(callback):
    text = f'Ещё раз привет, {callback.from_user.first_name}, я - бот <b>Cool Pictures</b>! \n\nЯ помогу Вам найти интересные картинки по вашему вкусу. Для начала выберите настроение картинки из плиток в низу экрана.👇'
    if callback.data == 'vent-1':
        markup1 = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Продолжить', callback_data='да')
        markup1.add(btn1)
        bot.edit_message_text(f'Привет, {callback.from_user.first_name}! Вы выбрали <b>Русский</b> 🇷🇺 язык. <b>Продолжить?</b> \n\nIf you want to change your choice, write /lang', callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup1)

    elif callback.data == 'eng':
        markup2 = types.InlineKeyboardMarkup()
        btn2 = types.InlineKeyboardButton('Continue', callback_data='yes')
        markup2.add(btn2)
        bot.edit_message_text(f'Hello, {callback.from_user.first_name}! You chose <b>English</b> 🇬🇧 language. <b>Continue?</b> \n\nЕсли вы хотите изменить свой выбор, напишите /lang', callback.message.chat.id, callback.message.message_id, parse_mode='html', reply_markup=markup2)

    if callback.data == 'да':
        text = text
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn1r = types.KeyboardButton('Весёлое 😄')
        btn2r = types.KeyboardButton('Нейтральное 😐')
        btn3r = types.KeyboardButton('Грустное 😔')
        markup.add(btn1r)
        markup.add(btn2r)
        markup.add(btn3r)
        bot.send_message(callback.from_user.id, text, parse_mode='html', reply_markup=markup)