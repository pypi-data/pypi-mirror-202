import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ConnectionError, ProxyError

import requests
from bs4 import BeautifulSoup
import time
import random


HEADER = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


class Session(requests.Session):
    def __init__(self, max_retries=3, headers=None, sleep=0, timeout=60):
        super().__init__()
        self.mount('https://', HTTPAdapter(max_retries=Retry(total=5, backoff_factor=1, status_forcelist=[504])))
        self.headers = headers if headers else HEADER
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
        return self.get(url, **kwargs).json()

    def get_soup(self, url, **kwargs):
        return BeautifulSoup(self.get(url, **kwargs).text, features='lxml')
