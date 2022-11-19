from telebot import TeleBot, types
import settings
from os import remove


def button_create(*button_name_list, resize_keyboard=True, one_time_keyboard=True, row_width=1, is_command=True):
    """
    Создание кнопок и добавление их на клавиатуру.
    :param button_name_list: String->List, Название кнопок
    :param resize_keyboard: Boolean, Переназначение размера
    :param one_time_keyboard: Boolean, Кнопки исчезают после итерации.
    :param row_width: Integer, Количество кнопок в строке
    :param is_command: Boolean, Флаг команды
    :return:
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard,
                                       row_width=2)

    command_char = '/' if is_command else ''

    for button_name in button_name_list:
        button = types.KeyboardButton(f'{command_char}{button_name}')
        markup.add(button)

    return markup


def get_image_from_message(bot, message):
    """
    Сохранение принятых изображений
    """
    with open(f'{settings.IMG_PATH}/{message.chat.id}', 'wb') as user_photo:  # TODO
        user_photo.write(bot.download_file(bot.get_file(message.photo[-1].file_id).file_path))
    return True
