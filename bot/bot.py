#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from aiogram.types.bot_command import BotCommand
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import asyncio
import logging


from helper_classes.assistant import MinorOperations
from database.mongodb.mongo_init import create_db
from routers import trade_offer_wish
from data_storage.emojis_chats import Emojis
from routers import main_router


helper = MinorOperations()
emojis = Emojis()


async def set_commands_and_description(bot: Bot) -> None:
    commands = [
    BotCommand(
        command="/cancel",
        description="Отменить действие"
		),
    BotCommand(
        command="/menu",
        description="Меню"
		)
    ]
    #description_one = f"{emojis.HELLO} Привет, я бот для обратной связи с сотрудниками NBC!\n"
    description_one = f'''
            Добро пожаловать в наш бот для сбора ваших бизнес-идей и предложений! Мы стремимся к развитию, и ваша обратная связь очень важна для нас.

Как это работает:
- Просто отправьте свою идею или пожелание в чат с ботом
- Ваше предложение будет рассмотрено командой, и вы получите обратную связь
- Лучшие идеи мы внедрим в нашу работу

Давайте вместе двигаться вперед! Отправляйте идеи прямо сейчас и помогайте улучшить нашу компанию.
    '''
    description_two = f"Добро пожаловать в наш бот для сбора ваших бизнес-идей и предложений!"
    await bot.set_my_description(description=description_one)
    await bot.set_my_short_description(short_description=description_two)
    await bot.set_my_commands(commands)
    
    
async def main():
    load_dotenv()#Потом убрать надо
    
    logging.basicConfig(level=logging.INFO)
    
    bot = Bot(token=await helper.get_tg_token())
    dp = Dispatcher()
    
    await set_commands_and_description(bot)
    dp.include_router(main_router.router)
    dp.include_router(trade_offer_wish.router)

    await create_db()
    logging.info("BOT STARTED")
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
    