import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    """
    Распознает текст из изображения с помощью Tesseract OCR.
    """
    try:
        image = Image.open(image_path)  # Открываем изображение
        text = pytesseract.image_to_string(image, lang='eng')  # Распознаём текст
        return text
    except Exception as e:
        print(f"Ошибка OCR: {e}")
        return ""
