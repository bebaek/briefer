import requests


def get_news(api_key):
    """Return news headline string"""
    url = f'https://newsapi.org/v2/top-headlines?country=us&apikey={api_key}'
    response = requests.get(url).json()
    selected_news = response['articles'][:3]
    titles = []
    urls = []
    for news in selected_news:
        titles += [news['title']]
        urls += [news['url']]

    # Compose HTML content
    msg = '<p><b>News Headlines</p>\n\n'
    for title, url in zip(titles, urls):
        msg += f'<p><a href="{url}">{title}</a></p>\n'

    # Add attribution:
    msg += (
        '<p>Powered by <a href="https://newsapi.org">NewsAPI.org</a></p>\n\n')
    return msg
