import os
import logging
import time
from pydub import AudioSegment
import speech_recognition as sr
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables first
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Check if API key exists
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OPENAI_API_KEY environment variable not found!")
    # Fallback to a placeholder that will cause a clear error if used
    api_key = "MISSING_API_KEY"

# Set FFmpeg paths
FFMPEG_PATH = r"C:\Users\mobol\Downloads\ffmpeg-2025-05-19-git-c55d65ac0a-essentials_build\ffmpeg-2025-05-19-git-c55d65ac0a-essentials_build\bin"
AudioSegment.converter = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
AudioSegment.ffmpeg = os.path.join(FFMPEG_PATH, "ffmpeg.exe")
AudioSegment.ffprobe = os.path.join(FFMPEG_PATH, "ffprobe.exe")

# Verify FFmpeg paths
if not os.path.exists(AudioSegment.converter):
    logging.error(f"FFmpeg not found at: {AudioSegment.converter}")
if not os.path.exists(AudioSegment.ffprobe):
    logging.error(f"FFprobe not found at: {AudioSegment.ffprobe}")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def convert_mp3_to_wav(mp3_path,wav_path ):
    audio = AudioSegment.from_mp3(mp3_path)

    audio.export(wav_path, format="wav")

    logging.info(f"Converted {mp3_path} to {wav_path}")


def split_audio(wav_path, chunk_length_ms=60000):
    audio = AudioSegment.from_wav(wav_path)
    chunks=[audio[i:i+ chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks


def transcibe_audio_chunk(chunk, chunk_index):
    chunk_path = f"chunk_{chunk_index}.wav"
    chunk.export(chunk_path, format="wav")

    try:
        with open(chunk_path, 'rb') as audio_file:
            # Updated OpenAI API call
            response = client.audio.transcriptions.create(
                model="whisper-1",  # Fixed typo in model name
                file=audio_file
            )
            text = response.text  # New response format

    except Exception as e:
        logging.error(f"An error has occurred with chunk {chunk_index} : {e}")
        text = ""

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


async def summarize_text(text):
    try:
        # Updated OpenAI API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "you are a helpful assistant"},
                {"role": "user", "content": f"Summarize the following text in one sentence: {text}"}
            ]
        )
        summary = response.choices[0].message.content.strip()
        logging.info(f"Summary: {summary}")
        return summary
        
    except Exception as e:
        logging.error(f"An error occurred during text summarization: {e}")
        return "Summary generation failed"

def cleanup_old_files(directory: str, max_age_hours: int = 24):
    """Remove files older than max_age_hours in the specified directory"""
    current_time = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Check if file is older than max_age_hours
        if os.path.isfile(file_path) and current_time - os.path.getmtime(file_path) > max_age_hours * 3600:
            os.remove(file_path)
            logging.info(f"Removed old file: {file_path}")



