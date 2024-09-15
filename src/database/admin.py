from pymongo import MongoClient
from datetime import datetime, timedelta
import yaml
import hashlib
import os

m = hashlib.sha256()
client = MongoClient("mongodb://localhost:27017/")

root_dir = "C:/Users/TarunKumarChaubey/Documents/Learning/FastAPI"
DBConfig = yaml.safe_load(open(os.path.join(root_dir,"config/mongodb.yaml"),"r"))
database = DBConfig['Database']
ImagesUploaded = DBConfig['Collection']['ImagesUploaded']
UserDatabase = DBConfig['Collection']['UserDatabase']
ActiveUsers = DBConfig['Collection']['ActiveUsers']
AdminDB = DBConfig['Collection']['Admin']

client = MongoClient("mongodb://localhost:27017/")

async def is_valid_user(email, database = database, collection = AdminDB):
    if client.get_database(database).get_collection(collection).find_one({"EmailID": email}):
        return "User Added"
    else:
        return "User Not Exist"

async def add_user(email: str, user_id: str, password, database = database, collection = AdminDB):
    client.get_database(database).get_collection(collection).insert_one({
    "EmailID": f"{email}",
    "UserID": f"{user_id}",
    "Password": f"{password}"
    })

async def remove_user(email, database = database, collection = AdminDB):
    if is_valid_user(email):
        client.get_database(database).get_collection(collection).delete_one({"EmailID": email})
        return "User Removed"
    else:
        return "User Not Exist"

async def change_password(email:str, password:str ,collection = UserDatabase):
    if client.get_database(database).get_collection(collection).find_one({"EmailID": email}):
        client.get_database(database).get_collection(collection).update_one(
                            {"EmailID": email},
                            {"$set": {"Password": f"{password}"}})
        return "Password Updated Successfully"
    else:
        return "User Not Exist"
