from django.contrib.auth.base_user import BaseUserManager


# Passwords are managed by Mojang
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, uuid, **extra_fields):
        if not uuid:
            raise ValueError('The given UUID must be set')
        user = self.model(uuid=uuid, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, uuid, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(uuid, **extra_fields)

    def create_superuser(self, uuid, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(uuid, **extra_fields)
