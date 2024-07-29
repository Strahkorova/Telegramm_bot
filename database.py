from config import bot
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import random

# строка подключения
sqlite_database = "sqlite:///galaxy.db"

# создаем движок SqlAlchemy
engine = create_engine(sqlite_database)

#Создаем класс сессии
Session = sessionmaker(autoflush=False, bind=engine)

# создаем базовый класс для моделей
class Base(DeclarativeBase): pass


# создаем модель, объекты которой будут храниться в бд
class Tezis_base(Base):
    __tablename__ = "tezis"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    rule = Column(String)


#https://metanit.com/python/database/3.3.php


class Database:

    def insert(message, NAME, TEXT):
        with Session(autoflush=False, bind=engine) as db:
            # создаем объект Person для добавления в бд
            rule = Tezis_base(name=NAME, rule=TEXT)
            db.add(rule)  # добавляем в бд
            db.commit()  # сохраняем изменения

        bot.send_message(message.chat.id, 'Твоя помощь галактике неоценима! Благодарю тебя юный джедай!')

    def select_all(message):
        with Session(autoflush=False, bind=engine) as db:
            # получение всех объектов
            Low = db.query(Tezis_base).all()
            if Low != []:
                text = ''
                for tx in Low:
                    text += f'ID: {tx.id}\n Автор: {tx.name}\n Правило: {tx.rule}\n\n'
                bot.send_message(message.chat.id, text)
            else:
                bot.send_message(message.chat.id, 'База данных пуста!')

    def delete_all(message):
        with Session(autoflush=False, bind=engine) as db:
            n = db.query(Tezis_base).count()
            while n != 0:
                rule_all = db.query(Tezis_base).filter(Tezis_base.id==n).first()
                db.delete(rule_all)  # удаляем объект
                n -= 1
            db.commit()  # сохраняем изменения
        bot.send_message(message.chat.id, 'Жестоко наказание верхного магистра! Бойся юный падаван!')

    def delete(message, id):
        with Session(autoflush=False, bind=engine) as db:
            rule_all = db.query(Tezis_base).filter(Tezis_base.id == id).first()
            db.delete(rule_all)  # удаляем объект
            db.commit()  # сохраняем изменения
        bot.send_message(message.chat.id, 'Жестоко наказание верхного магистра! Бойся юный падаван!')

    def select_one(message, id):
        with Session(autoflush=False, bind=engine) as db:
            one_tezis = db.get(Tezis_base, id)
            text = f'ID: {one_tezis.id}\n Автор: {one_tezis.name}\n Правило: {one_tezis.rule}\n\n'
            bot.send_message(message.chat.id, text)

    def select_random(message):
        with Session(autoflush=False, bind=engine) as db:
            m = random.randint(1, db.query(Tezis_base).count())
            one_tezis = db.get(Tezis_base, m)
            bot.send_message(message.chat.id, 'Мудрость светлой стороны')
            text = f'Автор: {one_tezis.name}\n Правило: {one_tezis.rule}'
            bot.send_message(message.chat.id, text)
