#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import asyncio
import logging

from aiogram.types.bot_command import BotCommand
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from models.long_messages import LONG_DESCRIPTION, SHORT_DESCRIPTION

from admin import admin_panel
from routers import commands, registration, actions, trade_offer_wish

from config import TELEGRAM_TOKEN

async def set_commands_and_description(bot: Bot) -> None:
    commands = [
        BotCommand(
            command="/menu",
            description="Меню"
	    ),
        BotCommand(
            command="/cancel",
            description="Отменить действие"
	    )
    ]

    await bot.set_my_description(description=LONG_DESCRIPTION)
    await bot.set_my_short_description(short_description=SHORT_DESCRIPTION)
    await bot.set_my_commands(commands)
    
    
async def main():
    load_dotenv()#Для локальных запусков
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%m %H:%M')
    
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    
    await set_commands_and_description(bot)
    
    dp.include_router(commands.router)
    dp.include_router(registration.router)
    dp.include_router(actions.router)
    dp.include_router(admin_panel.router)

    dp.include_router(trade_offer_wish.router)

    logging.warning("BOT STARTED")
    
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())
    
