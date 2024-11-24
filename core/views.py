from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
import os
from django.conf import settings
from .utils import (
    extract_text_from_image,
    clean_text,
    split_text_by_language,
    extract_contacts,
    save_text_to_txt,
    save_text_to_docx
)


class OCRAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    SUPPORTED_LANGUAGES = ['eng', 'rus', 'spa']  # Поддерживаемые языки

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('image')
        languages = request.data.get('languages', 'eng')  # Языки через запятую
        file_format = request.data.get('format', 'txt')  # Формат файла

        # Проверки входных данных
        if not file_obj:
            return Response({"error": "Не загружено изображение"}, status=400)

        lang_list = languages.split(',')
        for lang in lang_list:
            if lang not in self.SUPPORTED_LANGUAGES:
                return Response({"error": f"Неподдерживаемый язык: {lang}"}, status=400)

        if file_format not in ['txt', 'docx']:
            return Response({"error": "Формат файла должен быть 'txt' или 'docx'"}, status=400)

        # OCR с поддержкой нескольких языков
        lang_param = '+'.join(lang_list)  # Преобразуем языки в формат Tesseract
        raw_text = extract_text_from_image(file_obj, lang=lang_param)

        # Очистка текста
        cleaned_text = clean_text(raw_text)

        # Разделение текста по языкам
        text_by_language = split_text_by_language(raw_text)

        # Извлечение контактов
        contacts = extract_contacts(" ".join(text_by_language.get("eng", [])))

        # Генерация уникальных имен файлов
        raw_file_path = os.path.join(settings.MEDIA_ROOT, f'raw_text.{file_format}')
        cleaned_file_path = os.path.join(settings.MEDIA_ROOT, f'cleaned_text.{file_format}')

        # Сохраняем файлы
        try:
            if file_format == 'txt':
                save_text_to_txt(raw_file_path, raw_text)
                save_text_to_txt(cleaned_file_path, cleaned_text)
            elif file_format == 'docx':
                save_text_to_docx(raw_file_path, raw_text)
                save_text_to_docx(cleaned_file_path, cleaned_text)
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")  # Отладочный вывод

        # Проверяем, созданы ли файлы
        if not os.path.exists(raw_file_path) or not os.path.exists(cleaned_file_path):
            return Response({"error": "Файлы не были сохранены"}, status=500)

        # Возвращаем результат
        return Response({
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "text_by_language": text_by_language,
            "contacts": contacts,
            "raw_file_path": raw_file_path,
            "cleaned_file_path": cleaned_file_path,
        })
