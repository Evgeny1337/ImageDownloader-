from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from fetch_nasa_images import fetch_archive
from downloader import download_picture, get_file_extension
from dotenv import load_dotenv
from os import environ
import requests


def start(update: Update, context: CallbackContext) -> None:
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


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main():
    load_dotenv()
    tg_token = environ['TELEGRAM_TOKEN']
    nasa_api_key = environ['NASA_API_KEY']
    updater = Updater(tg_token, use_context=True)
    updater.dispatcher.bot_data['nasa_api_key'] = nasa_api_key

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
