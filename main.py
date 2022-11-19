from telebot import TeleBot, types
from back import button_create, get_image_from_message
import settings
import dl
from os import path

bot = TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start', 'Спасибо!', 'Назад'])
def bot_start(message):
    """
    Стартовое меню.
    :param message: bot.dict
    """
    hello_message = 'Пожалуйста' if message.text == '/Спасибо!' else 'Здравствуйте'
    markup = button_create('Помощь', 'Распознавание_текста')
    bot.send_message(message.chat.id, f'{hello_message} {message.from_user.first_name}.\nВыберите команду:',
                     reply_markup=markup)


@bot.message_handler(commands=['Распознавание_текста'])
def bot_text_recognition_step_one(message):
    """
    Триггер команды '/Распознавание_текста'.
    :param message: bot.dict
    """
    bot.send_message(message.chat.id, f'Отправьте изображение:')


@bot.message_handler(content_types=['photo'])
def bot_text_recognition_step_two(message):
    """
    Триггер отправки фотографий в чат.
    На этом этапе сохраняет изображение.
    """
    get_image_from_message(bot, message)
    markup = button_create('русский', 'english')
    bot.send_message(message.chat.id, 'Выберите язык текста:', reply_markup=markup)


@bot.message_handler(commands=['русский', 'english'])
def bot_text_recognition_step_three(message):
    """
    Триггер команды выбора языка.
    Проверяет наличие изображения с предыдущего шага и отправляет на обработку.
    """
    img_path = path.join(settings.IMG_PATH, str(message.chat.id))
    if path.exists(img_path):
        markup = button_create('Спасибо!')
        bot.send_message(message.chat.id, dl.image_recognition(img_path, message.text),
                         reply_markup=markup)
    else:
        markup = button_create('Назад')
        bot.send_message(message.chat.id, f'Не получил от вас изображение.Повторите попытку.',
                         reply_markup=markup)


@bot.message_handler(commands=['Помощь'])
def bot_help_command(message):
    """
    Раздел помощи.
    """
    markup = button_create('Спасибо!')
    bot.send_message(message.chat.id, settings.BOT_HELP_MESSAGE, reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
