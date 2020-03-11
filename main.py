from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


def get_stats():
    url = 'https://www.nhl.com/player/phil-kessel-8473548'
    response = simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        stats = set()
        for li in html.find_all('li', class_="player-bio__item"):
            for stat in li.text.split('span'):

                if len(stat) > 0:
                    stats.add(stat.strip())
        return list(stats)

    raise Exception('Error retrieving contents at {}'.format(url))


if __name__ == '__main__':
    print('\nGetting Phils stats....')
    stats = get_stats()
    print('...done.\n')

    for stat in stats:
        print(stat)

    print('\n\n')
    stats = [x.replace('\n', ' ') for x in stats]
    stats = [x.replace(' ', '') for x in stats]

    print('-----------------------------------')
    print(stats)
    print('-----------------------------------')

    for stat in stats:
        print(stat)
