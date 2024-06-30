# -*- coding: UTF-8 -*-

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Union
from bson import ObjectId
import logging

from helper_classes.assistant import MinorOperations

helper = MinorOperations()

class Interaction:
	#def __init__(self) -> None:
	#	mongo_client = AsyncIOMotorClient(f'mongodb://localhost:27017')
	#	self.__db = mongo_client['request_bot']
	#	self.__current_data = self.__db['general_info_about_user'] # Коллекция с данны
	#	self.__happened_events =  self.__db['happened_events']
 
	def __init__(self,) -> None:
		user = helper.get_mongo_login()
		password = helper.get_mongo_password()
		mongo_client = AsyncIOMotorClient(f'mongodb://{user}:{password}@mongodb:27017')
		self.__db = mongo_client['request_bot']
		self.__current_data = self.__db['general_info_about_user'] # Коллекция с данны
		self.__happened_events =  self.__db['happened_events']
  
  
	async def find_data(self, filter: dict) -> dict:

		return await self.__current_data.find_one(filter)


	async def update_data(self, filter: dict, update: int) -> None:
		
		await self.__current_data.update_one(filter, update)


	async def get_data(self, user_id: int, type_data: str) -> Union[int, str, float, dict]:#!~~~!!!!!
		filter_by_id = {'tg_id': user_id}
		result = await self.__current_data.find_one({'users': {'$elemMatch': filter_by_id}},{'users.$': 1})

		return result['users'][0][f'{type_data}']


	async def document_the_event(self, type_event, current_date, phone, fullname, tg_addr, info):
		document = await self.__happened_events.find_one({"_id": ObjectId("66606c99b6c0c50083906389")})
		new_order = {
			'type_event': type_event,
   			'date_of_creation': current_date,
			'creator_addr': f'@{tg_addr}',
			'creator name': fullname,
			'phone': phone,
			'info': info
     	}
		update = {'$push': {'events': new_order}}
		response = await self.__happened_events.update_one(document, update)
		logging.info(f'Journal event are {response.acknowledged}')