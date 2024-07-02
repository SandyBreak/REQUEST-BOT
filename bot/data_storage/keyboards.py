# -*- coding: UTF-8 -*-

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardButton, InlineKeyboardBuilder

from data_storage.emojis_chats import Emojis


emojis = Emojis()

class Keyboards:
    def __init__(self) -> None:
        pass


    async def possibilities_keyboard(self):
        builder = InlineKeyboardBuilder(
            markup=[
                [
                    InlineKeyboardButton(text=f"{emojis.BUSINESS} Предложить бизнес-идею", callback_data='trade_offer')
                ],
                [
                    InlineKeyboardButton(text=f"{emojis.IDEA} Рассказать о своих пожеланиях, предложениях", callback_data='suggest_idea')
                ]
            ],
        )
        return builder
    
    async def phone_access_request(self):
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Да", request_contact=True)
                ],
                [
                    KeyboardButton(text="Нет")
                ]
            ],
            resize_keyboard=True, one_time_keyboard=True
            )
        return keyboard