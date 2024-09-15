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


async def is_valid_user(Emaild: str, collection_name = UserDatabase):
    if client.get_database(database).get_collection(collection_name).find_one({"EmailID": Emaild}):
        return True
    return False

async def insert_user(email: str, user_id: str, password, collection_name = UserDatabase):
    if client.get_database(database).get_collection(collection_name).find_one({"EmailID": email}):
        return f"User Already with Id {email}"
    
    client.get_database(database).get_collection(collection_name).insert_one({
    "EmailID": f"{email}",
    "UserID": f"{user_id}",
    "Password": f"{password}"
    })
    return "User Added Successfully"
    
async def create_token(email:str , password:str, session_collection = ActiveUsers, collection_name = UserDatabase):
    if is_valid_user(email):
        UserData = client.get_database(database).get_collection(collection_name).find_one({"EmailID": email})
        if str(password) ==  UserData['Password']:
            Token = hashlib.sha256(UserData['Password'].encode('utf-8')).hexdigest()
            client.get_database(database).get_collection(session_collection).insert_one({
                "EmailID": UserData['EmailID'],
                "UserID": UserData['UserID'],
                "Token": f"{Token}",
                "createdAt": datetime.utcnow(),  # Add a field for the creation time
                "expireAt": datetime.utcnow() + timedelta(seconds=10)  # Set TTL field to expire after 30 seconds
            })
            return Token
        else:
            return "Wrong Password"
        
async def delete_token(email:str ,session_collection = ActiveUsers):
    if client.get_database(database).get_collection(session_collection).find_one({"EmailID": email}):
        client.get_database(database).get_collection(session_collection).delete_one({"EmailID": email})
        return "Logout Successfully"
    else:
        return "User Already Logout"
    

async def update_user_password(email:str, password:str ,session_collection = UserDatabase):
    if client.get_database(database).get_collection(session_collection).find_one({"EmailID": email}):
        client.get_database(database).get_collection(session_collection).update_one(
                            {"EmailID": email},
                            {"$set": {"Password": f"{password}"}})
        return "Password Updated Successfully"
    else:
        return "User Not Exist"