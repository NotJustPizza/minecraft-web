import json
import hashlib
import urllib.parse
import requests
import concurrent.futures
import logging
from ..settings import JSONAPI as JSONAPI_SETTINGS


class JsonAPI:
    logger = logging.getLogger(__name__)
    urls = []

    def __init__(
        self,
        host: str = None,
        port: int = None,
        username: str = None,
        password: str = None,
        settings_name: str = 'default'
    ):
        settings = JSONAPI_SETTINGS[settings_name]

        self.host = host if host else settings['HOST']
        self.port = port if port else settings['PORT']
        self.username = username if username else settings['USERNAME']
        self.password = password if password else settings['PASSWORD']

    # Weird sha256 encoded auth token
    def make_key(self, method: str) -> str:
        string = self.username + method + self.password
        encoded_string = string.encode('utf-8')

        return hashlib.sha256(encoded_string).hexdigest()

    # Weird url containing json data as param
    def make_url(self, method: str, args: list = None) -> str:
        # Urlencode our request json data
        encoded_json = urllib.parse.quote(self.make_json(method, args))

        return f"http://{self.host}:{self.port}/api/2/call?json={encoded_json}"

    # Weird json data needed to make request
    def make_json(self, method: str, args: list = None) -> str:
        data = {
            'name': method,
            'arguments': args,
            'key': self.make_key(method),
            'username': self.username
        }

        return json.dumps(data)

    # Add url that will be called later
    def add_url(self, method: str, args: list = None) -> None:
        url = self.make_url(method, args)
        self.urls.append(url)

    def load_url(self, url: str, timeout: int) -> requests.Response:
        return requests.get(url, timeout=timeout)

    # Call urls in parallel and return responses
    def call(self, timeout: int = 2) -> dict:
        results = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_i = {executor.submit(self.load_url, url, timeout): i for i, url in enumerate(self.urls)}
            for future in concurrent.futures.as_completed(future_to_i):
                i = future_to_i[future]

                # By default we return None is something goes wrong
                results[i] = None

                try:
                    # We don't use multicalls feature so we only need first element from json
                    data = future.result().json()[0]

                    # I know it's weird, but it's how this API works
                    if not data['is_success'] or data['result'] != 'success':
                        self.logger.error(f"JsonAPI: Request not successful")
                    else:
                        # Actual result is in success field
                        results[i] = data['success']
                except Exception as exception:
                    self.logger.error(f"JsonAPI: {exception}")

        return results
