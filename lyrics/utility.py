
import logging

from pydub import AudioSegment

import speech_recognition as sr

import openai 
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO

import requests
import os

logging.basicConfig(level=logging.INFO)

def convert_mp3_to_wav(mp3_path,wav_path ):
    audio = AudioSegment.from_mp3(mp3_path)

    audio.export(wav_path, format="wav")

    logging.info(f"Converted {mp3_path} to {wav_path}")


def split_audio(wav_path, chunk_length_ms=60000):
    audio = AudioSegment.from_wav(wav_path)
    chunks=[audio[i:i+ chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks


def transcibe_audio_chunk(chunk,chunk_index ):
    chunk_path =f"chunk_{chunk_index}.wav"

    chunk.export(chunk_path, format="wav")


    try: 
        with open(chunk_path, 'rb') as audio_file:
            response = openai.Audio.transcribe(
                model="whispper-1",
                file=audio_file
            )

            text= response['text']

    except Exception as e:
        logging.error(f"An error has occurred with chunk {chunk_index} : {e}")

        text =""

    finally: 
        os.remove(chunk_path)

    return text

        
def transcibe_wav_to_text(wav_path):
    chunks= split_audio(wav_path)
    full_text=""
    
    
    for i , chunk in enumerate(chunks):
        chunk_text = transcibe_audio_chunk(chunk, i)
        full_text += chunk_text + " "
        
        
    logging.info(f"Transcribed text: {full_text}")
    
    return full_text.strip()




########################################



