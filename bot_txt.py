import telebot
import os

def search_files(keywords):
    #directory = r"\Путь к директории\" # Тут лежат Ваши файлики
    files = []

    # В даном примере мы выполняем поиск только по .txt файлам внутри папки
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            # utf-8 позволяет нам искать русские слова
            with open(os.path.join(directory, file), "r", encoding="utf-8") as f:
                # .lower() позволяет выполнять поиск, который не чувствителен к регистру
                contents = f.read().lower()
                if all(keyword.lower() in contents for keyword in keywords):
                    files.append(file)
    return files



# Инициализация бота с токеном
bot = telebot.TeleBot("{Ваш токен}")


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Я найду все твои секретики")


# Выполняйте запрос по типу /search пароль
@bot.message_handler(commands=['search'])
def search(message):

    # Исключает из поиска саму команду
    keywords = message.text.split()[1:]

    # Если вы не внесли ключевые слова
    if not keywords:
        bot.reply_to(message, "Пожалуйста, укажите ключевые слова для поиска")
    else:
        # Если файлики с таким текстом не нашлись
        files = search_files(keywords)
        if not files:
            bot.reply_to(message, "Файлы не найдены")
        # Если файлики с таким текстом нашлись
        else:
            bot.reply_to(message, "Найдены файлы: " + ", ".join(files))

bot.polling()