import argparse

from urllib.error import URLError
from urllib.request import urlopen


def parse_cli_opts():
    """
    Returns Namespace object with parsed cli arguments
    """
    description = 'PointLoma - A Python library to execute Lighthouse and ' \
                  'export the results of running performance tests against ' \
                  'different Kolibri URLs'

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('url', help='Url to test against')
    parser.add_argument('-hl', '--headless', help='Run in headless mode',
                        required=False, default=True)
    parser.add_argument('-r', '--runs', help='Number of test runs',
                        required=False, default=1, type=int)
    parser.add_argument('-o', '--output-path', help='Path to csv file output',
                        required=False)
    parser.add_argument('-v', '--verbose', help='Increase output verbosity',
                        action='store_true')
    return parser.parse_args()


def check_url(url):
    """
    Return True if the specified URL is reachable and return False if the URL
    is malformed or not reachable
    """
    try:
        urlopen(url)
        return True
    except ValueError:
        return False  # URL not well formatted
    except URLError:
        return False  # URL doesn't seem to be reachable
