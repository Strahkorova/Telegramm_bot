from dataclasses import dataclass


@dataclass(frozen=True)
class Messages:

    def start(mess):
        return (f'Привет юный падаван, {mess.from_user.first_name}! Мудрость от Йоды "Светлая сторона силы путь верный к могуществу инженера!" Да прибудет с тобой сила!')


