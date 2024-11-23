from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import extract_text_from_image

class OCRAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """
        Загружает изображение и возвращает распознанный текст.
        """
        file_obj = request.FILES.get('image')
        if not file_obj:
            return Response({"error": "Не загружено изображение"}, status=400)

        # Сохраняем файл временно
        text = extract_text_from_image(file_obj)
        return Response({"text": text})

