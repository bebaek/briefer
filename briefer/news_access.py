import requests

TIMEOUT = 10


def get_news(api_key):
    """Return news headline string"""

    url = f'https://newsapi.org/v2/top-headlines?country=us&apikey={api_key}'
    response = requests.get(url, timeout=TIMEOUT).json()
    selected_news = response['articles'][:3]
    titles = []
    urls = []
    for news in selected_news:
        titles += [news['title']]
        urls += [news['url']]

    # Return new contents
    return titles, urls
