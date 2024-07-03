from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я бот. Используй команды /add, /subtract, /multiply, /divide.')

def add(update: Update, context: CallbackContext) -> None:
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        result = num1 + num2
        update.message.reply_text(f'Результат: {result}')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /add <число1> <число2>')

def subtract(update: Update, context: CallbackContext) -> None:
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        result = num1 + num2
        update.message.reply_text(f'Результат: {result}')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /subtract <число1> <число2>')

def multiply(update: Update, context: CallbackContext) -> None:
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        result = num1 * num2
        update.message.reply_text(f'Результат: {result}')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /multiply <число1> <число2>')

def divide(update: Update, context: CallbackContext) -> None:
    try:
        num1 = float(context.args[0])
        num2 = float(context.args[1])
        if num2 == 0:
            update.message.reply_text('Ошибка: деление на ноль.')
        else:
            result = num1 / num2
            update.message.reply_text(f'Результат: {result}')
    except (IndexError, ValueError):
        update.message.reply_text('Использование: /divide <число1> <число2>')

def main() -> None:
    updater = Updater('7336100479:AAE_KgTsKoCwMe1rctfOIDtfw0HgOnLzk4E')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("subtract", subtract))
    dispatcher.add_handler(CommandHandler("multiply", multiply))
    dispatcher.add_handler(CommandHandler("divide", divide))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()