import cloudinary
import cloudinary.uploader
import cloudinary.api

from pymongo import MongoClient
from decouple import config

cloudinary.config( 
        cloud_name = config("CLOUD_NAME"), 
        api_key = config("API_KEY"), 
        api_secret = config("API_SECRET"),
        secure = True,
)


def db_uploader():
    return cloudinary.uploader.upload


def db_deleter():
    return cloudinary.uploader.destroy


def get_mongodb():
    mongo_client = MongoClient(config("MONGO_URL"))
    return mongo_client["autocertify"]


