# -*- coding: UTF-8 -*-

from aiogram.fsm.state import State, StatesGroup
     
class TradeOfferWish(StatesGroup):
    """
    Состояния для заполнения запроса
    """
    get_info = State()
    get_contact_and_send_order = State()
    
    
class RegUserStates(StatesGroup):
    """
    Состояния для регистрации пользователя
    """
    get_fio = State()
