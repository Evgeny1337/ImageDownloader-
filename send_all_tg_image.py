import time
from telegram import Bot
from telegram.ext import Updater
from dotenv import load_dotenv
from os import environ, listdir, path
import argparse
import random


def main():
    MAX_PHOTO_SIZE = 20 * 1024 * 1024
    load_dotenv()
    tg_token = environ['TELEGRAM_TOKEN']
    try:
        chat_id = environ['TELEGRAM_CHAT_ID']
    except KeyError:
        print('Не добавлен id чата в котороый необхожимо отправить изображение\n' +
              'Используйте скрипт bot.py и команду /savechatid в канале, куда необходимо отправить изображение')

    parser = argparse.ArgumentParser(
        prog='Загрузчик изображений из папки images')

    parser.add_argument(
        '-a', '-all_photo', type=float, help='Введите время задержки отправки между файлами в минутах', required=True)
    args = parser.parse_args()
    updater = Updater(tg_token, use_context=True)
    dispatcher = updater.dispatcher

    try:
        while True:
            updater.start_polling()
            files = [file for file in listdir('./images/')]
            random.shuffle(files)
            for file in files:
                if path.isfile('./images/' + file) and path.getsize('./images/' + file) > 0 and path.getsize('./images/' + file) <= MAX_PHOTO_SIZE:
                    with open('./images/' + file, 'rb') as image:
                        dispatcher.bot.send_photo(photo=image, chat_id=chat_id)
                else:
                    print('Ошибка, файл не открывается, {}'.format(file))
            time.sleep(args.a)
            print("Прошло {} минут!".format(args.a))
    except KeyboardInterrupt:
        print("Остановка программы...")
        print("Программа завершена.")
        exit(0)


if __name__ == '__main__':
    main()
