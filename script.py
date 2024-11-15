import requests
from os import environ
from urllib.parse import urlparse
from os.path import split
from dotenv import load_dotenv

# rAUUvqhIde30nmxchRXyaIsaxTJK1GckfqaNfCUK


def get_file_extension(url):
    file_name = split(urlparse(url).path)
    return file_name[1]


def download_picture(url, file_path):
    response = requests.get(url=url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(url):
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


def fetch_nasa_pictures(url, count, api_key):
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


def fetch_nasa_epic_pictures(url, api_key):
    params = {'api_key': api_key}
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    for picture in response.json():
        picture_full_date = picture['date'].split(' ')[0]
        picture_date = picture_full_date.split('-')
        picture_name = picture['image']
        yield 'https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png?api_key={}'.format(picture_date[0], picture_date[1], picture_date[2], picture_name, api_key)


def main():
    load_dotenv()
    nasa_api_key = environ['NASA_API_KEY']
    try:
        picture_spacex_urls = fetch_spacex_last_launch(
            'https://api.spacexdata.com/v5/launches/5eb87ce4ffd86e000604b338')

    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(
            "Ошибка получения изображений spacex: ", err)
    try:
        picture_nasa_urls = fetch_nasa_pictures(
            'https://api.nasa.gov/planetary/apod', count=10, api_key=nasa_api_key)
    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(
            "Ошибка получения изображений nasa: ", err)
    try:
        pictures_earth_nasa_url = fetch_nasa_epic_pictures(
            url='https://api.nasa.gov/EPIC/api/natural/images', api_key=nasa_api_key)
    except requests.exceptions.HTTPError as err:
        raise requests.exceptions.HTTPError(
            "Ошибка получения изображений земли с сайта nasa: ", err)
    for url in picture_spacex_urls:
        try:
            download_picture(
                url, './images/{}'.format(get_file_extension(url)))
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError("Ошибка: ", err)
    for url in picture_nasa_urls:
        try:
            download_picture(
                url, './images/{}'.format(get_file_extension(url)))
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError("Ошибка: ", err)
    for url in pictures_earth_nasa_url:
        download_picture(
            url, './images/{}'.format(get_file_extension(url)))


if __name__ == '__main__':
    main()
