# -*- coding: UTF-8 -*-

import logging

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums import ParseMode
from aiogram import Router, F, Bot

from admin.admin_logs import send_log_message

from models.text_maps import choice_message_map, get_info_message_map
from models.user_keyboards import UserKeyboards
from models.admin_chats import AdminChats
from models.states import TradeOfferWish
from models.emojis import Emojis

from services.postgres.create_event_service import CreateEventService
from services.postgres.user_service import UserService

from utils.assistant import MinorOperations

from exceptions.errors import UserNotRegError

router = Router()


@router.callback_query(F.data.in_(["trade_offer", "suggest_idea"]))
async def start_create_event(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await callback.answer()
    await state.update_data(type_event=callback.data)
    try:
        await UserService.check_user_exists(callback.from_user.id)

        await CreateEventService.delete_temporary_data(callback.from_user.id)
        await CreateEventService.init_new_event(callback.from_user.id, callback.data)
        
        await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f'{Emojis.SUCCESS} {choice_message_map[callback.data]} {Emojis.SUCCESS}')
        delete_message = await callback.message.answer(f'{get_info_message_map[callback.data]}')

        await state.set_state(TradeOfferWish.get_info)
    except UserNotRegError:
        delete_message = await bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.message_id, text=f"{Emojis.ALLERT} Вы не зарегистрированы! {Emojis.ALLERT}\nДля регистрации введите команду /start")
    
    await state.update_data(message_id=delete_message.message_id)


@router.message(F.text, StateFilter(TradeOfferWish.get_info))
async def get_info(message: Message, state: FSMContext) -> None:

    await CreateEventService.save_data(message.from_user.id, 'info', message.text)
    phone_access_request_keyboard = await UserKeyboards.phone_access_request()
    
    await message.answer(f'Согласны ли вы предоставить свой номер телефона?', reply_markup=phone_access_request_keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True))
    
    await state.set_state(TradeOfferWish.get_contact_and_send_order)

        
@router.message(F.contact | F.text, StateFilter(TradeOfferWish.get_contact_and_send_order))
async def get_contact_and_send_order(message: Message, state: FSMContext, bot: Bot) -> None:
    phone_number = message.contact.phone_number if message.contact else 'Не указан'
    type_event = (await state.get_data()).get('type_event')
    await CreateEventService.save_data(message.from_user.id, 'phone', phone_number)
    order_message = await MinorOperations.fill_event_data(message.from_user.id, phone_number, type_event)
    
    try:
        if message.from_user.id == 5890864355:
            message_log = await bot.send_message(AdminChats.BASE, order_message, parse_mode=ParseMode.HTML)
        else:
            message_log = await bot.send_message(AdminChats.LARISA, order_message, parse_mode=ParseMode.HTML)
        if (delete_message_id := (await state.get_data()).get('message_id')): await bot.delete_message(chat_id=message.chat.id, message_id=delete_message_id)
        await message.answer(f'{Emojis.SUCCESS} Ваше предложение успешно отправлено! {Emojis.SUCCESS}\nМы рассмотрим его в ближайшее время и дадим вам обратную связь. Спасибо, что помогаете нам развиваться!', reply_markup=ReplyKeyboardRemove())
        await  CreateEventService.save_created_event(message.from_user.id)
    except Exception as e:
        message_log = await message.answer(f'{Emojis.FAIL} Произошла какая то ошибка и запрос не отправлен, пожалуйста, свяжитесь с администратором по адресу: @global_aide_bot')
        logging.critical(e)
        
    await state.clear()
    if message_log: await send_log_message(message, bot, message_log)