from os.path import split
import requests
from urllib.parse import urlparse


def get_file_extension(url):
    file_name = split(urlparse(url).path)
    return file_name[1]


def download_picture(url, file_path):
    response = requests.get(url=url)
    response.raise_for_status()
    if '.' in file_path.split('/')[-1]:
        with open(file_path, 'wb') as file:
            file.write(response.content)


def download_nasa_epic_picture(url, file_path, api_key):
    params = {'api_key': api_key}
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    if '.' in file_path.split('/')[-1]:
        with open(file_path, 'wb') as file:
            file.write(response.content)
