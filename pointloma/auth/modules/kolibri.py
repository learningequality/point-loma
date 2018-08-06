"""
Custom Point Loma authentication module for Kolibri project
https://github.com/learningequality/kolibri

This module is required to have a `get_headers` function which should simply
return a dictionary containing the HTTP headers of the authenticated user
you wish to run the Point Loma audits with
"""

import requests


def get_headers(username, password, base_url):
    # Prepare dictionary with username and password fields
    data = {'username': username, 'password': password}

    # Send a HTTP request to the /user endpoint to retrieve cookies we'll use
    # to actually perform the authentication
    r = requests.get('{base_url}/user/'.format(base_url=base_url))

    # Make sure to support older Kolibri versions in which the session cookie
    # was named differently
    session_key = 'kolibri' if 'kolibri' in r.cookies else 'sessionid'

    # Extract CSRF and session cookies
    csrf_token = r.cookies['csrftoken']
    session_id = r.cookies[session_key]

    # Generate headers dictionary to use for authentication process
    login_headers = {
        'X-CSRFToken': csrf_token,
        'Cookie': '{session_key}={session_id}; csrftoken={csrf_token}'.format(
            session_key=session_key,
            session_id=session_id,
            csrf_token=csrf_token)}

    # Send POST HTTP request to `/api/session` with the username and password
    # fields and using the above generated headers dictionary
    r = requests.post('{base_url}/api/session/'.format(base_url=base_url),
                      data=data, headers=login_headers)

    # Finally, generate the dict with headers of a logged in user
    return {
        'X-CSRFToken': r.cookies['csrftoken'],
        'Cookie': '{session_key}={session_id}; csrftoken={csrf_token}'.format(
            session_key=session_key,
            session_id=r.cookies[session_key],
            csrf_token=r.cookies['csrftoken'])}
