from django.urls import path
from .views import OCRAPIView, serve_document

urlpatterns = [
    path('api/ocr/', OCRAPIView.as_view(), name='ocr_api'),
    path('media/<str:file_name>/', serve_document, name='serve_document'),
]
