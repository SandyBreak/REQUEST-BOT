# -*- coding: UTF-8 -*-

from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums import ParseMode
from aiogram import Router, F, Bot
from datetime import datetime
import logging


from database.mongodb.interaction import Interaction
from helper_classes.assistant import MinorOperations
from data_storage.keyboards import Keyboards
from data_storage.states import TradeOfferWish
from data_storage.emojis_chats import *


helper = MinorOperations()
bank_of_keys = Keyboards()
mongodb = Interaction()
chat_name = ChatNames()
router = Router()
emojis =Emojis()



@router.callback_query(F.data == "trade_offer")
async def enter_fio_employee(callback: CallbackQuery, state: FSMContext) -> None:
    filter_by_id = {'users.tg_id': callback.message.from_user.id}
    update = {'$set': {'users.$.type_message': 0}}
    await mongodb.update_data(filter_by_id, update)
    
    await callback.message.answer(f'Выбрано: {emojis.BUSINESS} Предложить бизнес-идею')
    await callback.message.answer(f'Поделитесь вашей бизнес-идеей:', reply_markup=ReplyKeyboardRemove())    
    await callback.answer()
    
    await state.set_state(TradeOfferWish.get_contacts)
    
@router.callback_query(F.data == "suggest_idea")
async def enter_fio_employee(callback: CallbackQuery, state: FSMContext) -> None:
    filter_by_id = {'users.tg_id': callback.message.from_user.id}
    update = {'$set': {'users.$.type_message': 1}}
    await mongodb.update_data(filter_by_id, update)

    await callback.message.answer(f'Выбрано: {emojis.IDEA} Рассказать о своих пожеланиях, предложениях')
    await callback.message.answer(f'Расскажите о ваших предложениях или пожеланиях:', reply_markup=ReplyKeyboardRemove())    
    await callback.answer()
    
    await state.set_state(TradeOfferWish.get_contacts)


@router.message(F.text, StateFilter(TradeOfferWish.get_contacts))
async def enter_office(message: Message, state: FSMContext) -> None:
    filter_by_id = {'users.tg_id': message.from_user.id}
    update = {'$set': {'users.$.secondary_data': message.text}}
    await mongodb.update_data(filter_by_id, update)
    
    keyboard = await bank_of_keys.phone_access_request()    
    
    await message.answer(f'Согласны ли вы предоставить свой номер телефона?', reply_markup=keyboard)
    
    await state.set_state(TradeOfferWish.send_order)

        
        
@router.message(F.contact | F.text, StateFilter(TradeOfferWish.send_order))
#@router.message(F.text, StateFilter(TradeOfferWish.send_order))
async def send_data(message: Message, state: FSMContext, bot: Bot) -> None:
    contact = message.contact
    if contact:
        phone_number = contact.phone_number
    else:
        phone_number = 'Не указан'
    
    name_order = await mongodb.get_data(message.from_user.id, 'secondary_data')
    type_order = await mongodb.get_data(message.from_user.id, 'type_message')
    print(type_order)
    order_message = await helper.fill_event_data(phone_number, message.from_user.full_name, message.from_user.username, name_order, int(type_order))
        
    success_flag = 0
    
    try:
        await bot.send_message(chat_id=chat_name.LARISA, text=order_message, parse_mode=ParseMode.HTML)
        success_flag = 1
    except Exception as e:
        logging.error(e)
    
    if success_flag:
        await message.answer('Ваше предложение успешно отправлено! Мы рассмотрим его в ближайшее время и дадим вам обратную связь. Спасибо, что помогаете нам развиваться!', reply_markup=ReplyKeyboardRemove())
        await  mongodb.document_the_event(type_order, datetime.now().strftime("%d-%m-%Y %H:%M"), phone_number, message.from_user.full_name, message.from_user.username, name_order)
    else:
        await message.answer('Извините, произошла ошибка при отправке вашего запроса. Пожалуйста, попробуйте еще раз. Если проблема сохраняется, свяжитесь с администратором по адресу @raptor_f_22', reply_markup=ReplyKeyboardRemove())
    
    await state.clear()
