from telegram import Bot
from dotenv import load_dotenv
from os import environ, listdir, path
import argparse
import random


def main():
    load_dotenv()
    tg_token = environ['TELEGRAM_TOKEN']
    try:
        chat_id = environ['TELEGRAM_CHAT_ID']
    except KeyError:
        print('Не добавлен id чата в котороый необхожимо отправить изображение\n' +
              'Используйте скрипт bot.py и команду /savechatid в канале, куда необходимо отправить изображение')

    bot = Bot(token=tg_token)
    parser = argparse.ArgumentParser(prog='Загрузчик одного изображения из папки images',
                                     description="Вы можете получить изображение по его имени из папки images\nлибо рандломное изображение из данной директории")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-o', '-one_picture', type=str,
                       help='Отправить изображение по имени')
    group.add_argument('-r', '-randome_picture', action='store_true',
                       help='Отправить рандомное изображение')
    args = parser.parse_args()

    if args.o:
        is_file = path.isfile('./images/' + args.o)
        if is_file:
            bot.send_photo(photo=open(
                './images/' + args.o, 'rb'), chat_id=chat_id)
        else:
            print('Такого файал не существует')
    elif args.r:
        files = [file for file in listdir('./images/')]
        if files:
            random_file = random.choice(files)
            bot.send_photo(photo=open(
                './images/' + random_file, 'rb'), chat_id=chat_id)
        else:
            print('Папка images пуста, заполните ее любым из доступных скриптов')


if __name__ == '__main__':
    main()
