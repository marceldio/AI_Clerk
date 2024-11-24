from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import extract_text_from_image, clean_text
from django.http import JsonResponse
import os
from django.conf import settings
from .utils import save_text_to_txt, save_text_to_docx


class OCRAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    SUPPORTED_LANGUAGES = ['eng', 'rus', 'spa']

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('image')
        language = request.data.get('language', 'eng')  # По умолчанию английский
        file_format = request.data.get('format', 'txt')  # Формат файла

        if not file_obj:
            return Response({"error": "Не загружено изображение"}, status=400)

        if language not in self.SUPPORTED_LANGUAGES:
            return Response({"error": f"Неподдерживаемый язык: {language}"}, status=400)

        if file_format not in ['txt', 'docx']:
            return Response({"error": "Формат файла должен быть 'txt' или 'docx'"}, status=400)

        # Распознавание текста
        raw_text = extract_text_from_image(file_obj, lang=language)
        cleaned_text = clean_text(raw_text)

        # Генерируем пути для файлов
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
            "raw_file_path": raw_file_path,
            "cleaned_file_path": cleaned_file_path,
        })

