import argparse
import requests
from downloader import download_picture as download
from downloader import get_file_extension as filename


def fetch_pictures(launch_id='latest'):
    url = 'https://api.spacexdata.com/v5/launches/{}'.format(launch_id)
    response = requests.get(url)
    response.raise_for_status()
    picture_response = []
    if type(response.json()) is list:
        for url in response.json():
            if url['links']['flickr']['original']:
                picture_response.extend(url['links']['flickr']['original'])
    else:
        picture_response.extend(response.json()['links']['flickr']['original'])
    for picture_url in picture_response:
        yield picture_url


def main():
    parser = argparse.ArgumentParser(prog='Загрузчик изображений с сайта SPACEX',
                                     description="Вы можете получить изображение по его идентификатору, либо все последние запуски")

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '-all_picture', action='store_true',
                       help='Скачает все изображения последнего запуска')
    group.add_argument('-f', '-find_picture', type=str,
                       help='Передайте id запуска, скачает все изображения из данного запуска')

    args = parser.parse_args()
    picture_spacex_urls = []
    try:
        if args.a:
            picture_spacex_urls = fetch_pictures()
        elif args.f:
            picture_spacex_urls = fetch_pictures(args.f)
    except requests.exceptions.HTTPError as err:
        print("Ошибка получения изображений spacex: ", err)
    for url in picture_spacex_urls:
        try:
            download(
                url, './images/{}'.format(filename(url)))
        except requests.exceptions.HTTPError as err:
            print("Ошибка: ", err)


if __name__ == '__main__':
    main()
