# -*- coding: UTF-8 -*-

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram import Router, Bot

from models.user_keyboards import UserKeyboards
from models.long_messages import HELLO_MESSAGE
from models.emojis import Emojis

from services.postgres.user_service import UserService

from exceptions.errors import UserNotRegError

router = Router()


@router.message(Command(commands=['menu', 'cancel']))    
async def cmd_menu(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Вывод меню
    """
    if (delete_message_id := (await state.get_data()).get('message_id')): await bot.delete_message(chat_id=message.chat.id, message_id=delete_message_id)
    await state.clear()
    try:
        await UserService.check_user_exists(message.from_user.id)
    
        delete_message = await message.answer(f"{Emojis.TIME} Отмена...", ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
        await bot.delete_message(chat_id=delete_message.chat.id, message_id=delete_message.message_id)
    
        possibilities_keyboard = await UserKeyboards.possibilities_keyboard()
        await message.answer(HELLO_MESSAGE, ParseMode.HTML, disable_web_page_preview=True, reply_markup=possibilities_keyboard.as_markup())
        
    except UserNotRegError:
        delete_message = await message.answer(f"{Emojis.ALLERT} Вы не зарегистрированы! {Emojis.ALLERT}\nДля регистрации введите команду /start", reply_markup=ReplyKeyboardRemove())
    
    await state.update_data(message_id=delete_message.message_id)
