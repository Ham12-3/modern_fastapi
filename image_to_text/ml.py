# TODO 


# the AI model that will take image as a input and bring out ext as output 


import pytesseract
import numpy as np
import os
from PIL import Image


# Point to the executable, not just the directory
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text(image_path) -> str:
    image = Image.open(image_path)
    
    text = pytesseract.image_to_string(image)
    
    # Remove symbols and split by lines for better display 
    characters_to_remove = "!()@—*“>+-/,'|£#%$&^_~"
    
    text = ''.join(char for char in text if char not in characters_to_remove)
    
    text_lines = text.split('\n')
    return text_lines