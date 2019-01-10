import threading

import requests

import logger
from languages import LANG_CODE
from modules_manager import DynamicModule, Say, NM, EQ
from utils import REQUEST_ERRORS

NAME = 'forismatic'
CFG_RELOAD = {'settings': ('lang',)}
API = 1

DISABLE = False


class Main(threading.Thread):
    INTERVAL = 3600 * 12

    def __init__(self, cfg, log, owner):
        super().__init__()
        self.cfg = cfg
        self.log = log
        self.own = owner

        self.disable = False

        self._wait = threading.Event()
        self._work = False
        self._events = ('start_record', 'stop_record', 'start_talking', 'stop_talking', 'voice_activated')

    def start(self):
        self.reload()
        self._work = True
        super().start()

    def join(self, timeout=None):
        self._unsubscribe()
        self._work = False
        self._wait.set()
        super().join(timeout)

    def reload(self):
        self.disable = LANG_CODE.get('ISO') != 'ru'
        if self.disable:
            self._unsubscribe()
        else:
            self._subscribe()

    def stop(self):
        raise RuntimeError('Newer!')

    def run(self):
        while self._work:
            self._wait.wait(self.INTERVAL)
            if self._wait.is_set():
                self._wait.clear()
                continue
            if self.disable:
                continue
            try:
                msg = random_quotes()
            except RuntimeError as e:
                self.log(e, logger.WARN)
            else:
                self.own.say(msg)

    def _callback(self, *_):
        self._wait.set()

    def _mod_callback(self, *_):
        try:
            return Say(random_quotes())
        except RuntimeError as e:
            self.log(e, logger.WARN)

    def _subscribe(self):
        self.own.subscribe(self._events, self._callback)
        self.own.insert_module(DynamicModule(self._mod_callback, NM, ['скажи афоризм', EQ]))

    def _unsubscribe(self):
        self.own.unsubscribe(self._events, self._callback)
        self.own.extract_module(self._mod_callback)


def random_quotes():
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
