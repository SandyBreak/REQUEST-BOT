# -*- coding: UTF-8 -*-

from aiogram.fsm.state import State, StatesGroup
     
class TradeOfferWish(StatesGroup):
    get_contacts = State()
    send_order = State()