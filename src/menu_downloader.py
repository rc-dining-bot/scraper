import logging

import requests


def construct_menu_url(date):
    year = date.year
    timestamp = date.strftime('%y%m%d-%a')
    return f'https://uci.nus.edu.sg/ohs/wp-content/uploads/sites/3/{year}/01/{timestamp}-Daily-Menu.pdf'


def send_request_for_menu_pdf(url):
    # Spoof the user agent to (hopefully) get past Incapsula
    user_agent = ('Mozilla/5.0 (Windows NT 6.1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/35.0.1916.153 '
                  'Safari/537.36 '
                  'SE 2.X '
                  'MetaSr 1.0')
    headers = {
        'User-Agent': user_agent
    }
    try:
        response = requests.get(url, timeout=10, headers=headers)
    except requests.exceptions.ConnectionError as error:
        logging.error('Failed to establish connection')
        logging.error(error)
        return None
    except requests.exceptions.Timeout:
        logging.error('Request to %s timed out', url)
        return None

    # Handle possible errors
    status_code = response.status_code
    if status_code != 200:
        logging.error('%s returned %d', url, status_code)
        logging.error('Response: %s', response.content)
        return None

    content_type = response.headers['Content-Type']
    if content_type != 'application/pdf':
        # Didn't get what we want, probably blocked by Incapsula
        logging.error(
            'Failed to get menu from %s, got Content-Type %s', url, content_type)
        logging.error('Response: %s', response.content)
        return None

    return response


def download_menu_pdf(date, filepath=None):
    logging.debug('Attempting to get the menu for %s', date)

    # Send request
    url = construct_menu_url(date)
    response = send_request_for_menu_pdf(url)

    # If request is not successful, abort
    if not response:
        return None

    # Otherwise, save the pdf file

    # Use filename from the url if customized filename is given
    if filepath is None:
        filepath = url.split('/')[-1]

    with open(filepath, 'wb') as file:
        logging.info('Successfully downloaded menu for %s to %s',
                     date, filepath)
        file.write(response.content)

    return filepath
