import json
import os
import sys

from importlib import import_module


AUTH_DIR = os.path.join('pointloma', 'auth', )
AUTH_MODULES_DIR = os.path.join(AUTH_DIR, 'modules')
HEADERS_FILE_PATH = os.path.join(AUTH_DIR, 'headers.json')


def authenticate(auth_module, base_url):
    """
    Attempts to retrieve the authentication credentials for the user you
    you wish to use to perform the audits with
    """
    username = os.environ.get('POINTLOMA_USERNAME')
    password = os.environ.get('POINTLOMA_PASSWORD')

    if not username or not password:
        raise ValueError('Username and password are required.')

    sys.path.append(os.path.join(os.getcwd(), AUTH_MODULES_DIR))
    try:
        auth = import_module(auth_module)
    except ImportError:
        pass

    headers = auth.get_headers(username, password, base_url=base_url)
    if not headers:
        return None

    _write_headers_file(headers, HEADERS_FILE_PATH)
    return HEADERS_FILE_PATH


def _write_headers_file(headers, file_path):
    with open(file_path, 'w') as file:
        json.dump(headers, file)
