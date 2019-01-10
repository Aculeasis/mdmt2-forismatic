import requests

from modules_manager import DynamicModule, Say, NM, EQ
from utils import REQUEST_ERRORS

NAME = 'forismatic-say'
API = 99999


def Main(owner, **_):
    owner.insert_module(DynamicModule(forismatic_say, NM, ['скажи афоризм', EQ]))


def forismatic_say(*_):
    try:
        return Say(random_quotes())
    except RuntimeError as e:
        Say(e)


def random_quotes() -> str:
    params = {
        'method': 'getQuote',
        'format': 'json',
        'lang': 'ru',
        'key': '',
    }
    try:
        result = requests.post('http://api.forismatic.com/api/1.0/', params=params)
    except REQUEST_ERRORS as e:
        raise RuntimeError('Request error: {}'.format(e))
    if not result.ok:
        raise RuntimeError('Server error {}:{}'.format(result.status_code, result.reason))
    try:
        msg = result.json()['quoteText'][:200]
    except (TypeError, KeyError, ValueError) as e:
        raise RuntimeError('Parsing error: {}, {}'.format(e, result.text[:200]))
    if not msg:
        raise RuntimeError('Empty quote')
    return msg
