import argparse
import requests
from downloader import download_picture as download
from downloader import download_nasa_epic_picture as download_epic
from downloader import get_file_extension as filename
from os import environ
from dotenv import load_dotenv


def fetch_epic(url, api_key):
    params = {'api_key': api_key}
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    for picture in response.json():
        picture_full_date = picture['date'].split(' ')[0]
        picture_date = picture_full_date.split('-')
        picture_name = picture['image']
        yield 'https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png'.format(picture_date[0], picture_date[1], picture_date[2], picture_name)


def fetch_archive(url, count, api_key):
    params = {'api_key': api_key, 'count': count}
    response = requests.get(url, params=params)
    response.raise_for_status()
    picture_response = []
    if type(response.json()) is list:
        for url in response.json():
            picture_response.append(url['url'])
    else:
        picture_response.append(response.json()['url'])
    for picture_url in picture_response:
        yield picture_url


def main():
    load_dotenv()
    nasa_api_key = environ['NASA_API_KEY']
    parser = argparse.ArgumentParser(prog='Загрузчик изображений с сайта NASA',
                                     description="Вы можете получить изображение по его идентификатору, либо все последние запуски")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-с', '-count', type=str,
                       help='Получить изображения из архива NASA. Укажите количество изображений, необходимое для скачивания')
    group.add_argument('-e', '-earth', action='store_true',
                       help='Получить снимики земли NASA')
    picture_nasa_urls = []
    args = parser.parse_args()
    try:
        if args.с:
            picture_nasa_urls = fetch_archive(url='https://api.nasa.gov/planetary/apod',
                                              count=args.с, api_key=nasa_api_key)
        elif args.e:
            picture_nasa_epic_urls = fetch_epic(url='https://api.nasa.gov/EPIC/api/natural/images',
                                                api_key=nasa_api_key)
    except requests.exceptions.HTTPError as err:
        print("Ошибка получения изображений NASA: ", err)

    for url in picture_nasa_epic_urls:
        try:
            download_epic(
                url, './images/{}'.format(filename(url)), nasa_api_key)
        except requests.exceptions.HTTPError as err:
            print("Ошибка: ", err)

    for url in picture_nasa_urls:
        try:
            download(
                url, './images/{}'.format(filename(url)))
        except requests.exceptions.HTTPError as err:
            print("Ошибка: ", err)


if __name__ == '__main__':
    main()
