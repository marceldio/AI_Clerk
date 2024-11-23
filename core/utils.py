import re
from PIL import Image
import pytesseract

def extract_text_from_image(image_path):
    """
    Распознает текст из изображения с помощью Tesseract OCR.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang='eng')  # Сырые данные OCR
        return text
    except Exception as e:
        print(f"Ошибка OCR: {e}")
        return ""

def clean_text(text):
    """
    Убирает лишние символы и переносы строк.
    """
    # Удаляем лишние пробелы и переводим текст в одну строку
    cleaned_text = re.sub(r'\s+', ' ', text).strip()
    return cleaned_text
