# -*- coding: UTF-8 -*-

from aiogram.utils.keyboard import KeyboardButton, InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from models.emojis import Emojis

class UserKeyboards:
    def __init__(self) -> None:
        pass


    @staticmethod
    async def possibilities_keyboard() -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        
        builder.row(InlineKeyboardButton(text=f"{Emojis.BUSINESS} Предложить бизнес-идею", callback_data='trade_offer'))
        builder.row(InlineKeyboardButton(text=f"{Emojis.IDEA} Рассказать о своих пожеланиях, предложениях", callback_data='suggest_idea'))
        
        return builder
    
    
    @staticmethod
    async def phone_access_request() -> ReplyKeyboardBuilder:
        
        builder = ReplyKeyboardBuilder()
        
        builder.row(KeyboardButton(text="Да", request_contact=True))
        builder.row(KeyboardButton(text="Нет"))
        
        return builder