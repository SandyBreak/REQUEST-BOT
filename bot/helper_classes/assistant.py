# -*- coding: UTF-8 -*-

import os


class MinorOperations:
    def __init__(self) -> None:
        pass
    
    
    async def get_tg_token(self) -> str:
        return os.environ.get('TELEGRAM_TOKEN')
    
    
    def get_mongo_login(self) -> str:
        return os.environ.get('MONGO_INITDB_ROOT_USERNAME')
    
    
    def get_mongo_password(self) -> str:
        return os.environ.get('MONGO_INITDB_ROOT_PASSWORD')
    
    
    async def fill_event_data(self, phone: str, customer: str, tg_customer: str, order: str, type_order: int) -> str:
        types_order= [
            'Новая бизнес идея!',
            'Новое пожелание!'
        ]
        order_info = [
            'Идея',
            'Пожелание',
        ]

        new_order = f"""
        <b>{types_order[type_order]}</b>
        <b>Номер телефона:</b> {phone}
        <b>Сотрудник:</b> {customer}
        <b>Телеграмм сотрудника:</b> @{tg_customer}
        <b>{order_info[type_order]}:</b> {order}
        """
        return new_order
        