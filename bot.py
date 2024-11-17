# import telegram
# bot = telegram.Bot(token='8169604083:AAHTum4s0qw2LuratEnqYHu0U6sSkHIkqLg')
# print(bot.get_me())

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
from os import environ
# Функция для обработки команд /start


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'Привет! Я бот, который загружает фотографии космоса.')


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main():
    load_dotenv()
    tg_token = environ['TELEGRAM_TOKEN']
    updater = Updater(tg_token)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
