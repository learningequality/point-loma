"""
Custom Point Loma authentication module for Kolibri project
https://github.com/learningequality/kolibri

This module is required to have a `get_headers` function which returns HTTP
headers with an authenticated user you wish to use to run Point Loma audits
"""
import requests


def get_headers(url, username, password):
    # Prepare dictionary with username and password fields
    data = {'username': username, 'password': password}

    # Send a HTTP request to the /user endpoint to retrieve cookies we'll use
    # to actually perform the authentication
    r = requests.get('{url}/user/'.format(url=url))

    # Make sure to support older Kolibri versions in which the session cookie
    # was named differently
    session_key = 'kolibri' if 'kolibri' in r.cookies else 'sessionid'

    # Extract CSRF and session cookies
    csrf_token = r.cookies['csrftoken']
    session_id = r.cookies[session_key]

    # Generate headers dictionary to use for authentication process
    headers = {
        'X-CSRFToken': csrf_token,
        'Cookie': '{session_key}={session_id}; csrftoken={csrf_token}'.format(
            session_key=session_key,
            session_id=session_id,
            csrf_token=csrf_token)}

    # Send POST HTTP request to `/api/session` with the username and password
    # fields and using the above generated headers dictionary
    r = requests.post('{url}/api/session/'.format(url=url), data=data,
                      headers=headers)

    # Finally, return the dictionary with headers necessary to login to Kolibri
    return {
        'X-CSRFToken': r.cookies['csrftoken'],
        'Cookie': '{session_key}={session_id}; csrftoken={csrf_token}'.format(
            session_key=session_key,
            session_id=r.cookies[session_key],
            csrf_token=r.cookies['csrftoken'])}
