import sqlite3
import logging
import os
from config import bot
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

# строка подключения
sqlite_database = "sqlite:///galaxy.db"

# создаем движок SqlAlchemy
engine = create_engine(sqlite_database)


# создаем базовый класс для моделей
class Base(DeclarativeBase): pass


# создаем модель, объекты которой будут храниться в бд
class Person(Base):
    __tablename__ = "tezis"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    rule = Column(String)


https://metanit.com/python/database/3.3.php


class Database:

    def connect(message):
        conn = sqlite3.connect('db_thermo.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS tezis (id INT PRIMARY KEY, Name varchar(60), Text varchar(500))')
        conn.commit()
        cur.close()
        conn.close()

    def insert(message, NAME, TEXT):
        conn = sqlite3.connect('db_thermo.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO tezis (Name, Text) VALUES ('%s', '%s')" % (NAME, TEXT))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, 'Твоя помощь галактике неоценима! Благодарю тебя юный джедай!')

    def select_all(message):
        conn = sqlite3.connect('db_thermo.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM tezis')
        Low = cur.fetchall()

        text = ''
        for tx in Low:
            text += f'ID: {tx[0]}\n Автор: {tx[1]}\n Правило: {tx[2]}\n\n'
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, text)



    async def update_users(self, user_id: int, leagues: str):
        update_query = f"""Update leagues 
                              set leagues = "{leagues}" where id = {user_id}"""
        self._execute_query(update_query)
        logging.info(f"Leagues for user {user_id} updated")

    async def delete_users(self, user_id: int):
        delete_query = f"""DELETE FROM users WHERE id = {user_id}"""
        self._execute_query(delete_query)
        logging.info(f"User {user_id} deleted")