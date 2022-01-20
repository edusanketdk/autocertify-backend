from database import get_mongodb
from datetime import datetime
from bson import ObjectId



def mark_stage(session_id, stage):
    mongo_db = get_mongodb()
	
    mongo_db.data.update_one(
        {'_id': ObjectId(session_id)}, 
        {'$set': {'stage': stage, "time": datetime.now()}}, 
        upsert=True,
        )
    