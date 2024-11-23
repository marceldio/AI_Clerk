from django.urls import path
from .views import OCRAPIView

urlpatterns = [
    path('api/ocr/', OCRAPIView.as_view(), name='ocr_api'),
]
