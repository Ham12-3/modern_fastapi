from fastapi import FastAPI , File, UploadFile, HTTPException, Form

from fastapi.responses import FileResponse, HTMLResponse

from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

import os

from io import BytesIO
from pydub import AudioSegment
from PIL import Image
from dotenv import load_dotenv
import logging
import speech_recognition as sr

import openai

import requests

from schemas import LyricsPayload


load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# use logging
logging.basicConfig(level=logging.INFO)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


####################################################################################
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if not os.path.exists("static"):
    os.mkdirs('converted_files')



@app.get("/",response_class=HTMLResponse )
async def read_root():
    return templates.TemplateResponse("index.html",{"request": {}} )


@app.post("/uploadfile/")
async def create_upload_file(file:UploadFile=File(...), language: str= Form(...)):
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())


    # AUDIO PROCESSING 

    wave_file_location = f"converted_files/{file.filename.replace('.mp3', '.wav')}"


    # convert mp3 to wav 
   

