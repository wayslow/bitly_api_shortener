import os
from dotenv import load_dotenv
import requests

from urllib.parse import urlparse



def shorten_link(url, headers):
    bitly_url = 'https://api-ssl.bitly.com/v4/shorten'
    params = {"long_url": url}
    response = requests.post(bitly_url, json=params, headers=headers)
    response.raise_for_status()
    return response.json()['link']


def count_clicks(url, headers):
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary'
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()
    return clicks_count['total_clicks']


def is_bitlink(url, headers):
    bitly_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"
    response = requests.get(bitly_url, headers=headers)
    return response.ok


def main():
    load_dotenv()
    bitly_api_token = os.getenv('BITLY_API_TOKEN')
    headers = {'Authorization': "Bearer {}".format(bitly_api_token)}
    url = input("введите ссылку ")
    parse = urlparse(url)
    parse_url = f'{parse.netloc}{parse.path}'
    try:
        if is_bitlink(parse_url, headers):
            clicks = count_clicks(parse_url, headers)
            print(f"количество кликов:{str(clicks)}")
        else:
            bitlink = shorten_link(url, headers)
            print(bitlink)
    except requests.exceptions.HTTPError:
        print("нормально ссылку на пиши, чебурек")


if __name__ == '__main__':
    main()