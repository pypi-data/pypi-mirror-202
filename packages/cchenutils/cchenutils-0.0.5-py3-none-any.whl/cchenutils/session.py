import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ConnectionError, ProxyError, JSONDecodeError

from .dict import dict

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}


class Session(requests.Session):
    def __init__(self, max_retries=3, headers=None, sleep=0, timeout=60):
        super().__init__()
        self.mount('https://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1, status_forcelist=[504])))
        self.headers = headers if headers else HEADERS
        self.max_retries = max_retries
        self.sleep = sleep
        self.timeout = timeout

    def get(self, url, **kwargs):
        r"""Sends a GET request. Returns :class:`Response` object.
        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :rtype: requests.Response
        """
        kwargs.setdefault('allow_redirects', True)

        try:
            r = self.request("GET", url, **kwargs)
            if r.status_code == 200 or kwargs.get('_retry') == self.max_retries:
                return r
        except (ProxyError, ConnectionError):
            pass
        time.sleep(self.sleep)
        kwargs['_retry'] = kwargs.setdefault('_retry', 0) + 1
        return self.get(url, **kwargs)

    def get_json(self, url, **kwargs):
        return dict(self.get(url, **kwargs).json())

    def get_soup(self, url, **kwargs):
        return BeautifulSoup(self.get(url, **kwargs).text, features='lxml')

    def get_json_or_soup(self, url, **kwargs):
        r = self.get(url, **kwargs)
        try:
            return dict(r.json())
        except JSONDecodeError:
            return BeautifulSoup(r.text, features='lxml')
