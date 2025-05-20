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


import utility
from schemas import LyricsPayload
from utility import summarize_text, transcibe_wav_to_text, split_audio, convert_mp3_to_wav

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
    convert_mp3_to_wav(file_location, wave_file_location)
    lyrics = transcibe_wav_to_text(wave_file_location)
    
    os.remove(file_location)
    
    summary = await summarize_text(lyrics)
    
    return {"lyrics": lyrics, "summary": summary}


@app.post('/generate_image/')
async def generate_imaeg(payload: LyricsPayload):
    
    try: 
        api_key  = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            logging.error("API key not found")
            raise HTTPException(status_code=500, detail="API key not found")
        
        
        dalle_url = "https://api.openai.com/v1/images/generations"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        
        prompt = f"Generate an image based on this summary of a song:  {payload.lyrics}"
        
        if len(prompt)  > 1000:
            prompt = prompt[:1000]
            
        data = {"prompt": prompt,
                "size": "1024x1024",
                "n": 1}
        
        logging.info(f"Sending to OPenAI API with {data}")
        
        
        response = requests.post(dalle_url, headers=headers, json=data)
        
        logging.info(f"OpenAI api response : {response.status_code}")
        
        
        logging.info(f"OpenAI API response content: {response.text}")
        
        
        response.raise_for_status()
        image_url = response.json()['data'][0]['url']
        
        
        image_response = requests.get(image_url)
        
        image_response.raise_for_status()
        
        
        image= Image.open(BytesIO(image_response.content))
        
        
        if not os.path.exists("media"):
            os.makedirs("media")
        image_path = os.path.join("media", "generated_image.png")
        image.save(image_path)
        
        
        
        logging.info(f"Image saved at {image_path}")
        
        return {"image_path": image_path}
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {e}")
        
        raise HTTPException(status_code=500, detail=str(e))
    
    


@app.get("/media/generated_image.png")
async def get_generated_image():
    return FileResponse("media/generated_image.png")
        
        
    # convert mp3 to wav 
   

