from django.urls import path
from .views import ocr_view, serve_document


urlpatterns = [
    path('ocr/', ocr_view, name='ocr_view'),
    path('media/<str:file_name>/', serve_document, name='serve_document'),
]
