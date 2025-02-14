from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from django.conf import settings
import os
from .utils import (
    extract_text_from_image,
    split_text_by_language,
    extract_contacts,
    save_text_to_txt,
    save_text_to_docx,
    convert_pdf_to_images
)

SUPPORTED_LANGUAGES = ['eng', 'rus', 'spa']  # Поддерживаемые языки


def index_view(request):
    return render(request, 'core/index.html')


def ocr_view(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('image')  # Поддерживает как PDF, так и изображения
        languages = ['eng', 'rus', 'spa']
        file_format = request.POST.get('format', 'txt')  # Формат файла

        # Проверки входных данных
        if not file_obj:
            return JsonResponse({"error": "Не загружен файл"}, status=400)

        if file_format not in ['txt', 'docx']:
            return JsonResponse({"error": "Формат файла должен быть 'txt' или 'docx'"}, status=400)

        # Формируем параметр для Tesseract (например, 'eng+rus')
        lang_param = '+'.join(languages)

        # Проверяем, PDF или изображение
        file_name = file_obj.name.lower()
        if file_name.endswith('.pdf'):
            # Конвертация PDF в изображения
            pdf_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(pdf_path, 'wb') as f:
                f.write(file_obj.read())
            image_paths = convert_pdf_to_images(pdf_path)

            if not image_paths:
                return JsonResponse({"error": "Не удалось обработать PDF"}, status=500)

            # OCR для каждой страницы PDF
            raw_text = ""
            for image_path in image_paths:
                raw_text += extract_text_from_image(image_path, lang=lang_param) + "\n"

            # Удаление временных файлов изображений
            for image_path in image_paths:
                if os.path.exists(image_path):
                    os.remove(image_path)

            # Удаление исходного файла PDF
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        else:
            # OCR для изображения
            raw_text = extract_text_from_image(file_obj, lang=lang_param)

        # Разделение текста по языкам
        text_by_language = split_text_by_language(raw_text)

        # Извлечение контактов
        contacts = extract_contacts(" ".join(text_by_language.get("eng", [])))

        # Генерация уникальных имен файлов
        raw_file_path = os.path.join(settings.MEDIA_ROOT, f'raw_text.{file_format}')

        # Сохраняем файлы
        try:
            if file_format == 'txt':
                save_text_to_txt(raw_file_path, raw_text)
            elif file_format == 'docx':
                save_text_to_docx(raw_file_path, raw_text)
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")

        # Возвращаем результат
        return JsonResponse({
            "raw_text": raw_text,
            "text_by_language": text_by_language,
            "contacts": contacts,
            "raw_file_path": f"{settings.MEDIA_URL}raw_text.{file_format}",
        })

    return render(request, 'core/ocr_form.html')  # Замените на вашу HTML форму


def serve_document(request, file_name):
    """
    Обслуживает файлы .docx и .txt из папки MEDIA_ROOT.
    """
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    if os.path.exists(file_path):
        if file_name.endswith('.docx'):
            # Для .docx файлов
            response = FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        elif file_name.endswith('.txt'):
            # Для .txt файлов
            response = FileResponse(open(file_path, 'rb'), content_type='text/plain; charset=utf-8')
            response['Content-Disposition'] = f'inline; filename="{file_name}"'
        else:
            return JsonResponse({"error": "Неподдерживаемый формат файла"}, status=400)
        return response
    else:
        return JsonResponse({"error": "Файл не найден"}, status=404)
