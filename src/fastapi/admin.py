from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import json
from database.admin import add_user, remove_user, change_password, is_valid_user
router = APIRouter()

user_db = json.load(open("./data/user.json","r"))

@router.post("/check_user")
async def check_user(email: str):
    if is_valid_user(email):
        return {"status":"User Already exist"}
    else:
        return {"status":"User Not Exist"}

@router.post("/remove_admin")
async def remove_admin(email_id: str, password: int):
    token = await remove_admin(email_id, password)
    return {"token": token}

@router.post("/logout")
async def logout_user(email_id):
    status = await remove_admin(email_id)
    return {"status":status}

@router.post("/create_admin")
async def create_admin(email_id: str,user_name: str, password):
    status = await create_admin(email_id, user_name, password)
    return {"Status": status}

@router.post("/change_admin_password")
async def change_admin_password(emailid: str, password: int):
    status = await change_admin_password(emailid, password)
    return {"token": status}