import urllib.request, urllib.parse
import twurl
import json
import ssl
from urllib.error import HTTPError

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def input_data(data_type, condition="a", message=""):
    """
    (type, str, str) -> (object)
    Returns the valid for data_type and condition
    input with message for user
    """
    while True:
        try:
            a = data_type(input(message))
            if not eval(condition):
                raise ValueError
            return a
        except ValueError:
            print("Invalid input. Try again.")


def get_url(acct='pewdiepie'):
    if (len(acct) < 1): return None
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct})
    try:
        connection = urllib.request.urlopen(url, context=ctx)
    except HTTPError:
        return None

    return connection


def read_conn(connection):
    return json.loads(connection.read().decode())


def get_param(json):
    param = set()
    for i in json['users'][0]:
        lst = i.split(',')
        for j in lst:
            param.add(j)
    return param


def get_info(js, param):
    # print(json.dumps(js, indent=2))
    """
    headers = dict(connection.getheaders())
    print('Remaining', headers['x-rate-limit-remaining'])
    print(js['users'])
    """
    lst = []
    for u in js['users']:
        yield (u['screen_name'], u[param])




def main():
    global parameters
    acc = input('Enter the name of account: ')

    number = input_data(int, condition='a > 0', message='Enter the number of \
                        friends U wanna see info about: ')
    url = get_url(acc)

    js = read_conn(url)
    if not url:
        return "No such Twitter account. Try again"

    parameters = list(get_param(js))
    print('Choose the parameter u wanna see, f.g. status\nAvailable parameters:')
    for i in parameters:
        print(i, end=", ")
    print()

    param = input_data(str, message="Input the parameter: ", condition="a in parameters")

    get_info(js, param)


if __name__ == '__main__':
    main()