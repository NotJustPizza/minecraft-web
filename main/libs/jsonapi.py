import json
import hashlib
import urllib.parse
import requests
import logging
from ..settings import JSONAPI as JSONAPI_SETTINGS


class JsonAPI:
    logger = logging.getLogger(__name__)

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
    def call(self, method: str, args: list = None, timeout: int = 2) -> dict:
        url = self.make_url(method, args)
        result = None

        try:
            resp = requests.get(url, timeout=timeout)
            # Raise error if not 2xx
            resp.raise_for_status()
            # We don't use multiple calls, so we probably need only first response
            data = resp.json()[0]

            # I know it's weird, but it's how this API works
            if not data['is_success'] or data['result'] != 'success':
                self.logger.error(f"JsonAPI: Request not successful for {url}")
            else:
                # Actual result is in success field
                result = data['success']
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"JsonAPI: Http error - {e}")
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"JsonAPI: Connection error - {e}")
        except requests.exceptions.Timeout as e:
            self.logger.error(f"JsonAPI: Timeout - {e}")
        except requests.exceptions.TooManyRedirects as e:
            self.logger.error(f"JsonAPI: Too many redirects - {e}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"JsonAPI: Unknown error - {e}")

        return result
