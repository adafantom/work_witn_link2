import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import argparse


def shorten_link(headers, long_link):
    payload = {
        'long_url': long_link
    }
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['link']


def count_click(headers, user_bitlink):
    bitlink = urlparse(user_bitlink)
    payload = {
        "units": -1
    }
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink.netloc}{bitlink.path}/clicks/summary'
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(headers, user_link):
    bitlink = urlparse(user_link)
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink.netloc}{bitlink.path}'
    response = requests.get(url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_api_key = os.environ['BITLY_API_KEY']
    headers = {
        "Authorization": "Bearer {}".format(bitly_api_key)
    } 
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("user_link", help="user's link")
        args = parser.parse_args()
        user_link = args.user_link
        if is_bitlink(headers, user_link):
            return f'Количество посещений: {count_click(headers, user_link)}'
        else:
            return f'Сокращенная ссылка: {shorten_link(headers, user_link)}'
    except requests.exceptions.HTTPError as error:
        return "Can't get data from server:\n{0}".format(error)


if __name__ == "__main__":
    print(main())