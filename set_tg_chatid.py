from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv, set_key
from os import environ


def save_chatid(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    environ['TELEGRAM_CHAT_ID'] = str(chat_id)
    dotenv_path = '.env'
    set_key(dotenv_path, 'TELEGRAM_CHAT_ID', str(chat_id))
    update.message.reply_text(
        'Теперь фотографии будут отпарвляться в чат с id {}'.format(chat_id))


def main():
    load_dotenv()
    tg_token = environ['TELEGRAM_TOKEN']
    nasa_api_key = environ['NASA_API_KEY']
    updater = Updater(tg_token, use_context=True)
    updater.dispatcher.bot_data['nasa_api_key'] = nasa_api_key
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('savechatid', save_chatid))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
