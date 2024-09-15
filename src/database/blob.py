from pymongo import MongoClient
from datetime import datetime, timedelta
import yaml
from bson import ObjectId
import os

root_dir = "C:/Users/TarunKumarChaubey/Documents/Learning/FastAPI"
DBConfig = yaml.safe_load(open(os.path.join(root_dir,"config/mongodb.yaml"),"r"))
database = DBConfig['Database']
ImagesUploaded = DBConfig['Collection']['ImagesUploaded']
client = MongoClient("mongodb://localhost:27017/")

async def read_json(image_name, collection = ImagesUploaded, database = database):
    # print("Image Name From API : {}".format(image_name))
    if client.get_database(database).get_collection(collection).find_one({"filename":image_name}):
        document = client.get_database(database).get_collection(collection).find_one({"filename": image_name})
        return {str(k): v if not isinstance(v, ObjectId) else str(v) for k, v in document.items()} if document else "File does not exist"


def filter_json(uploader_user_name='', uploader_user_email_id='', usecase='',obj=[], skip=None, PAGE_SIZE=None, collection = ImagesUploaded, database = database):
    results = collection.find({
        "$or": [
            {"uploader_user_email_id": {"$exists": True}},
            {"uploader_user_name": {"$exists": True}},
            {"usecase": {"$exists": True}},
            {"obj": {"$exists": True}}
        ]}).skip(skip).limit(PAGE_SIZE)

    # Convert MongoDB cursor to list
    items = [item for item in results]

    return items


# async def upload_images():
#     pass

# async def read_images():
#     pass

# async def delete_images():
#     pass