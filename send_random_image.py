# kittybot/send_random_image.py
import requests
from telebot import TeleBot


bot = TeleBot(token='7633346829:AAFDFaK2gzulWb9YanoSbzQIY5sIOvI_dSU')
# Адрес API сохраним в константе:
URL = 'https://api.thecatapi.com/v1/images/search'  
chat_id = 1441970486

# Делаем GET-запрос к эндпоинту:
response = requests.get(URL).json()
# Извлекаем из ответа URL картинки:
random_cat_url = response[0].get('url')  

# Передаём chat_id и URL картинки в метод для отправки фото:
bot.send_photo(chat_id, random_cat_url) 