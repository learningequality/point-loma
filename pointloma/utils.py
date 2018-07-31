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
    parser.add_argument('url', help='url to test against')
    parser.add_argument('-r', '--runs', help='number of test runs',
                        required=False, default=1, type=int)
    parser.add_argument('-o', '--output-path', help='path to csv file output',
                        required=False)
    parser.add_argument('-v', '--verbose', help='increase output verbosity',
                        action='store_true')
    parser.add_argument('-a', '--auth-module',
                        help='authentication module to use',
                        required=False)
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
