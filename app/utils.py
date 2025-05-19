from openai import AsyncOpenAI  # Change from OpenAI to AsyncOpenAI
import os
from sqlalchemy.orm import Session
from models import TranslationRequest, TranslationResult, IndividualTranslations
from datetime import datetime
from database import SessionLocal
from typing import List
from dotenv import load_dotenv

load_dotenv()

# Create AsyncOpenAI client instead of regular OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def translate_text(text: str, language: str) -> str:
    """Translate text using OpenAI API with async client syntax"""
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following text to {language}:"},
            {"role": "user", "content": text},
        ]
    )
    return response.choices[0].message.content.strip()


async def process_translations(request_id: int, text: str, languages: List[str]):
    """Process translations for multiple languages and store in database"""
    # Get a database session (not using get_db as dependency since this is async)
    db = SessionLocal()
    try:
        for language in languages:
            translated_text = await translate_text(text, language)
            translation_result = TranslationResult(
                request_id=request_id, language=language, translated_text=translated_text
            )
            individual_translation = IndividualTranslations(
                request_id=request_id, translated_text=translated_text
            )
            db.add(translation_result)
            db.add(individual_translation)
            db.commit()
        
        request = db.query(TranslationRequest).filter(TranslationRequest.id == request_id).first()
        request.status = "completed"
        request.updated_at = datetime.utcnow()
        db.add(request)
        db.commit()
    finally:
        db.close()