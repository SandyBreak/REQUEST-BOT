from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import logging
from helper_classes.assistant import MinorOperations

helper = MinorOperations()

async def create_db():
    try:
        new_db = AsyncIOMotorClient(f'mongodb://localhost:27017')
        
        #user = helper.get_mongo_login()
        #password = helper.get_mongo_password()
        #new_db = AsyncIOMotorClient(f'mongodb://{user}:{password}@mongodb:27017')
        
        
        new_table = new_db["request_bot"]
        table1 = new_table['general_info_about_user']
        table2 = new_table['happened_events']
         
        obj1 = {"_id": ObjectId("665dd5e9513d61f6a8a66843"), "users": []}
        obj2 = {"_id": ObjectId("66606c99b6c0c50083906389"), "events": []}
        
        await table1.insert_one(obj1)
        await table2.insert_one(obj2)
        
    except Exception as e:
        logging.error(e)