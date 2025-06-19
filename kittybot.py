# kittybot/kittybot.py
import logging
import os
import requests

from telebot import TeleBot, types
from dotenv import load_dotenv


load_dotenv()

# Взяли переменную TOKEN из пространства переменных окружения:
secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

# bot = TeleBot(token='7633346829:AAFDFaK2gzulWb9YanoSbzQIY5sIOvI_dSU')
URL = 'https://api.thecatapi.com/v1/images/search'
# URL = ''


# Код запроса к thecatapi.com и обработку ответа обернём в функцию:
def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


# Добавляем хендлер для команды /newcat:
@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    # В ответ на команду /start
    # должно быть отправлено сообщение "Спасибо, что включили меня".
    chat = message.chat
    name = message.chat.first_name
    # Создаём объект клавиатуры:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # Создаём объект кнопки:
    button_newcat = types.KeyboardButton('/newcat')
    # Добавляем объект кнопки на клавиатуру:
    keyboard.add(button_newcat)
    # keyboard.row(  # Первая строка кнопок.
    #     types.KeyboardButton('Который час?'),  # Создаём первую кнопку в строке.
    #     types.KeyboardButton('Определи мой ip'),  # Создаём вторую кнопку в строке.
    # )
    # keyboard.row(  # Вторая строка кнопок.
    #     types.KeyboardButton('/random_digit'),  # Создаём кнопку в строке.
    # )
    bot.send_message(
        chat_id=chat.id,
        # text=f'Спасибо, что вы включили меня, {name}!',
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашел',
        # Отправляем клавиатуру в сообщении бота: передаём объект клавиатуры
        # в параметр reply_markup объекта send_message.
        # Telegram-клиент "запомнит" клавиатуру и будет отображать её в интерфейсе бота.
        reply_markup=keyboard,
        )

    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    # Из объекта message получаем данные о чате, из которого пришло сообщение,
    # и сохраняем эти данные в переменную chat.
    chat = message.chat
    # Получаем id чата:
    chat_id = chat.id
    # В ответ на любое текстовое сообщение в тот же чат
    # будет отправлено сообщение 'Привет, я KittyBot!'
    if 'кто' in message.text.lower():
        photo_path = r"C:\Users\Капибара\Documents\S00801-140936(1).jpg"
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)
    else:
        bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')


# Метод polling() запускает процесс; приложение начнёт
# отправлять регулярные запросы для получения входящих сообщений.
def main():
    bot.polling()


if __name__ == '__main__':
    main()
