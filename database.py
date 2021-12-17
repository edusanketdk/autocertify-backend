import cloudinary
import cloudinary.uploader
import cloudinary.api

from pymongo import MongoClient
from decouple import config


def db_uploader():
    cloudinary.config( 
        cloud_name = config("CLOUD_NAME"), 
        api_key = config("API_KEY"), 
        api_secret = config("API_SECRET"),
        secure = True,
    )
    return cloudinary.uploader.upload


def get_mongodb():
    mongo_client = MongoClient(config("MONGO_URL"))
    return mongo_client["autocertify"]


