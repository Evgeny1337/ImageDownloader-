import requests
from os import environ
from dotenv import load_dotenv
from downloader import get_file_extension, download_picture
from fetch_spacex_images import fetch_pictures as fetch_spacex_pictures
from fetch_nasa_images import fetch_archive, fetch_epic


def main():
    load_dotenv()
    nasa_api_key = environ['NASA_API_KEY']
    try:
        picture_spacex_urls = fetch_spacex_pictures('5eb87ce4ffd86e000604b338')

    except requests.exceptions.HTTPError as err:
        print("Ошибка получения изображений spacex: ", err)
    try:
        picture_nasa_urls = fetch_archive(
            'https://api.nasa.gov/planetary/apod', count=10, api_key=nasa_api_key)
    except requests.exceptions.HTTPError as err:
        print("Ошибка получения изображений nasa: ", err)
    try:
        pictures_earth_nasa_url = fetch_epic(
            url='https://api.nasa.gov/EPIC/api/natural/images', api_key=nasa_api_key)
    except requests.exceptions.HTTPError as err:
        print("Ошибка получения изображений земли с сайта nasa: ", err)
    for url in picture_spacex_urls:
        try:
            download_picture(
                url, './images/{}'.format(get_file_extension(url)))
        except requests.exceptions.HTTPError as err:
            print("Ошибка: ", err)
    for url in picture_nasa_urls:
        try:
            download_picture(
                url, './images/{}'.format(get_file_extension(url)))
        except requests.exceptions.HTTPError as err:
            print("Ошибка: ", err)
    for url in pictures_earth_nasa_url:
        try:
            download_picture(
                url, './images/{}'.format(get_file_extension(url)), nasa_api_key)
        except requests.exceptions.HTTPError as err:
            print("Ошибка: ", err)


if __name__ == '__main__':
    main()
