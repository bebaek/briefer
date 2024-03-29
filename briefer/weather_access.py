"""Weather access"""

import logging
import requests

from briefer.exceptions import ExternalAPIError

TIMEOUT = 10
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'  # noqa
headers = {'User-Agent': user_agent}

logger = logging.getLogger(__name__)


def get_weather(coordinates):
    """Get weather info via HTTP API from NWS.

    Parameters
    ----------
    coordinates : tuple of floats
        longitude and latitude. Use negative for south/west sides.

    Returns
    -------
    Weather forecast dictionary
    """

    # Validate/build a string with coordinate tuple
    lon = float(coordinates[0])
    lat = float(coordinates[1])

    res = {}

    # First, access with coordinates
    # FIXME: format
    url = f'https://api.weather.gov/points/{lon},{lat}'
    response = requests.get(url, headers=headers, timeout=TIMEOUT).json()

    # Get location zone
    loc = response['properties']['relativeLocation']['properties']
    res['location'] = f'{loc["city"]}, {loc["state"]}'

    # Second, access the linked forecast endpoint.
    url = response['properties']['forecast']
    response = requests.get(url, headers=headers, timeout=TIMEOUT).json()

    # Get some periods
    try:
        periods = response['properties']['periods']
    except KeyError as e:
        logger.warning(f'Unexpected weather API response:\n{response}')
        raise ExternalAPIError(f'{e} + \nresponse: {response}')

    res['forecasts'] = []
    for i in range(4):
        res['forecasts'] += [periods[i]]

    return res


if __name__ == '__main__':
    res = get_weather((30.2672, -97.7431))
    print(res)
