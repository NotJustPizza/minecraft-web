import json
import hashlib
import urllib.parse
import requests
from ..settings import JSONAPI as JSONAPI_SETTINGS


class JsonAPI:
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

    # Call JsonAPI and return response
    def call(self, method: str, args: list = None) -> dict:
        url = self.make_url(method, args)

        resp = requests.get(url)

        # We don't use multiple calls, so we probably need only first response
        return resp.json()[0]
