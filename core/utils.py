import re
from PIL import Image
import pytesseract
from docx import Document


def extract_text_from_image(image_path, lang='eng'):
    """
    Распознает текст из изображения с поддержкой нескольких языков.
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)  # Выбор языка
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


def save_text_to_txt(file_path, text):
    """
    Сохраняет текст в файл формата .txt.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Ошибка при сохранении в .txt: {e}")


def save_text_to_docx(file_path, text):
    """
    Сохраняет текст в файл формата .docx.
    """
    try:
        document = Document()
        document.add_paragraph(text)
        document.save(file_path)
    except Exception as e:
        print(f"Ошибка при сохранении в .docx: {e}")
