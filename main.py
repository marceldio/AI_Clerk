import os
from core.utils import save_text_to_txt, save_text_to_docx
import subprocess
import sys

def get_output_directory():
    """ Определяет, куда сохранять файлы. """
    if getattr(sys, 'frozen', False):  # Если это .exe, то используем путь рядом с исполняемым файлом
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_path, "output")
    os.makedirs(output_dir, exist_ok=True)  # Создаём папку, если её нет
    return output_dir

def open_file(file_path):
    """ Открывает файл в текстовом редакторе или Word. """
    try:
        if sys.platform == "win32":
            os.startfile(file_path)  # Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", file_path])  # macOS
        else:
            subprocess.run(["xdg-open", file_path])  # Linux
    except Exception as e:
        print(f"Ошибка открытия файла: {e}")

def main():
    """ Главная логика программы """
    text = input("Введите текст для сохранения: ")  # Запрос текста у пользователя
    output_dir = get_output_directory()

    # Сохранение в TXT
    txt_file_path = os.path.join(output_dir, "output.txt")
    save_text_to_txt(txt_file_path, text)
    print(f"Файл сохранён: {txt_file_path}")

    # Сохранение в DOCX
    docx_file_path = os.path.join(output_dir, "output.docx")
    save_text_to_docx(docx_file_path, text)
    print(f"Файл сохранён: {docx_file_path}")

    # Открываем файлы
    open_file(txt_file_path)
    open_file(docx_file_path)

if __name__ == "__main__":
    main()
