
from telegram.ext import CallbackContext
from telegram import Update, TelegramError
import random
import os
import requests
from downloader import download_picture, get_file_extension
from fetch_nasa_images import fetch_archive


def load_start_photo(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    nasa_api_key = context.bot_data.get('nasa_api_key')
    try:
        picture_url = fetch_archive(
            'https://api.nasa.gov/planetary/apod', 1, nasa_api_key)
    except requests.exceptions.HTTPError as err:
        update.message.reply_text("Ошибка сервера NASA {}".format(err))
    send_url = [url for url in picture_url]
    file_path = './images/{}'.format(get_file_extension(send_url[0]))
    try:
        download_picture(send_url[0], file_path)
    except requests.exceptions.HTTPError as err:
        update.message.reply_text("Ошибка загрузки фото {}".format(err))
    context.bot.send_photo(chat_id=chat_id, photo=open(file_path, 'rb'))


def load_all_images(context: CallbackContext):
    chat_id = context.job.context
    files = []
    directory = './images/'
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename != '.gitkeep' and os.path.isfile(file_path):
            files.append('{}{}'.format(directory, filename))
    random.shuffle(files)
    for file in files:
        try:
            context.bot.send_photo(chat_id=chat_id, photo=open(file, 'rb'))
        except TelegramError as e:
            context.bot.send_message(
                "Ошибка отпарвки изображения {}".format(e))
