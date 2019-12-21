import requests
import uuid
from django.core.exceptions import ValidationError

from .models import User


class AuthBackend(object):
    def authenticate(self, request, username: str = None, password: str = None) -> User:
        user_json, error_msg = self.get_mojang_user(request, username, password)

        if user_json is None:
            raise ValidationError(error_msg)
        else:
            try:
                user = User.objects.get(uuid=user_json['id'])
                # Update user name on login
                user.name = user_json['name']
                user.save(update_fields=['name'])
            except User.DoesNotExist:
                user = User(uuid=user_json['id'], name=user_json['name'])
                user.save()
            return user

    def get_user(self, user_uuid: uuid.UUID) -> User:
        try:
            return User.objects.get(pk=user_uuid)
        except User.DoesNotExist:
            return None

    def get_mojang_user(self, request, username: str, password: str) -> tuple:
        r = requests.post(
            'https://authserver.mojang.com/authenticate',
            json={
                'agent': {
                  'name': 'Minecraft',
                  'version': 1
                },
                'username': username,
                'password': password,
            }
        )

        if r.status_code == 200:
            return r.json()['selectedProfile'], None
        else:
            return None, r.json()['errorMessage']

