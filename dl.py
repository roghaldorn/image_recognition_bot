import pytesseract
from cv2 import cv2
from os import remove
from os.path import join
import settings

pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_PATH
config = settings.PYTESSERACT_CONFIG


def image_processing(message_path):
    """
    Преобразование цветового пространства изображения.
    :param message_path: String, путь к изображению.
    """
    user_img = cv2.imread(message_path)
    if user_img is None:
        return False
    return cv2.cvtColor(user_img, cv2.COLOR_BGR2RGB)


def image_recognition(message_path, lang):
    """
    Проверяет наличие изображения и производит
    Распознавание изображения с использованием tesseract ocr.
    :param message_path: String, путь к изображению.
    :param lang: String, язык текста.
    :return: String, текст с изображения.
    """
    user_lang = 'rus' if lang == '/русский' else 'eng'
    user_img = image_processing(message_path)

    if not user_img:
        return 'Ошибка при чтении изображения'

    image_text = pytesseract.image_to_string(user_img, lang=user_lang, config=config)  # TODO
    remove(message_path)

    return image_text
