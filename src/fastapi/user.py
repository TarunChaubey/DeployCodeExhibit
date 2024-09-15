from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import json
from src.database.user import create_token, insert_user,is_valid_user, delete_token, update_user_password

router = APIRouter()

user_db = json.load(open("./data/user.json","r"))

print(user_db[0])

@router.post("/check_user")
async def check_user(email: str):
    if is_valid_user(email):
        return {"status":"User Already exist"}
    else:
        return {"status":"User Not Exist"}

@router.post("/login_from_email_id")
async def login_from_email_id(email_id: str, password: int):
    token = await create_token(email_id, password)
    return {"token": token}

@router.post("/logout")
async def logout_user(email_id):
    status = await delete_token(email_id)
    return {"status":status}

@router.post("/sign_up")
async def sign_up(email_id: str,user_name: str, password):
    status = await insert_user(email_id, user_name, password)
    return {"Status": status}

@router.post("/forget_password")
async def forget_password(emailid: str, password: int):
    status = await update_user_password(emailid, password)
    return {"token": status}

