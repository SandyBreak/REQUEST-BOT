# -*- coding: UTF-8 -*-

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram import Router, F



from data_storage.keyboards import Keyboards
from data_storage.emojis_chats import Emojis


from database.mongodb.initialization import Initialization


router = Router()
bank_of_keys = Keyboards()
emojis = Emojis()


@router.message(Command(commands=['start', 'menu', 'cancel', ]))
async def cmd_start(message: Message, state: FSMContext)  -> None:
    await state.clear()
    user = Initialization(message.from_user.id, message.from_user.username)
    
    await user.init_user()
    await user.delete_user_meeting_data()
    
    keyboard = await bank_of_keys.possibilities_keyboard()
    
    hello_message = f"""
    Привет! Рад видеть тебя в нашем боте для сбора бизнес-идей и предложений. Мы ценим ваш вклад и хотим, чтобы ваши идеи были услышаны. Давайте вместе двигаться вперед и воплощать инновационные решения!
    """
    
    await message.answer(hello_message, ParseMode.HTML, disable_web_page_preview=True, reply_markup=keyboard.as_markup())