import json
import hashlib
import urllib.parse
import requests


class JsonAPI:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    # Weird sha256 encoded auth token
    def make_key(self, method: str) -> str:
        string = self.username + method + self.password
        encoded_string = string.encode('utf-8')

        return hashlib.sha256(encoded_string).hexdigest()

    # Weird url containing json data as param
    def make_url(self, method: str, args: dict = None) -> str:
        # Urlencode our request json data
        encoded_json = urllib.parse.quote(self.make_json(method, args))

        return f"http://{self.host}:{self.port}/api/2/call?json={encoded_json}"

    # Weird json data needed to make request
    def make_json(self, method: str, args: dict = None) -> str:
        data = {
            'name': method,
            'arguments': args,
            'key': self.make_key(method),
            'username': self.username
        }

        return json.dumps(data)

    # Call JsonAPI and return response
    def call(self, method: str, args: dict = None) -> dict:
        url = self.make_url(method, args)

        resp = requests.get(url)

        # We don't use multiple calls, so we probably need only first response
        return resp.json()[0]
