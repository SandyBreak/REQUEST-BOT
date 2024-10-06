# -*- coding: UTF-8 -*-

from models.text_maps import event_map

from services.postgres.create_event_service import CreateEventService
from services.postgres.user_service import UserService


class MinorOperations:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    async def fill_event_data(user_id: int, phone: str, type_event: int) -> str:
        
        user_data = await UserService.get_user_data(user_id)
        event_details = event_map[f'{type_event}']
        order_info = await CreateEventService.get_data(user_id, 'info')

        new_order = f"""
        <b>{event_details['type_event']}</b>
        <b>ФИО сотрудника:</b> {user_data.fio}
        <b>Телеграмм сотрудника:</b> @{user_data.nickname}
        <b>Номер телефона:</b> {phone}
        <b>{event_details['event_info']}:</b> {order_info}
        """
        return new_order
        