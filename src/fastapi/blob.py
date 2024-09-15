from fastapi import FastAPI, APIRouter, Query
from fastapi.responses import RedirectResponse
from fastapi import File, UploadFile
from typing import List
from src.utils import routemessage
from src.database.blob import read_json, filter_json
from typing_extensions import Optional

router = APIRouter()

@router.get("/read_json/")
async def read_json_of_image(image_name: str):
    status = await read_json(image_name)
    return {"Status": status}

@router.get("/filter_json/")
async def filter_json(page: Optional[int] = Query(default=1, ge=1),uploader_user_email_id: Optional[str] = None,uploader_user_name: Optional[str] = None,
                      usecase: Optional[str] = None, IsDetected: Optional[bool] = None):

    status = await filter_json(uploader_user_name, uploader_user_email_id, usecase)
    return {"Status": status}

@router.post("/upload_image")
async def upload_image(file: UploadFile):
    return {"Status": routemessage.UploadFile()}

@router.post("/upload_multiple_image")
async def upload_multiple_image(files: List[UploadFile] = File(...)):
    return {"Status": routemessage.UploadMultipleFile()}

@router.get("/read_image")
async def read_image():
    return {"Status": routemessage.ReadFiles()}

@router.get("/delete_image")
async def delete_image():
    return {"Status": "File Deleted"}