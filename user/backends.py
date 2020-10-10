from django.contrib.auth.hashers import check_password
from user.models import User
from django.contrib.auth.backends import BaseBackend


class EmailBackend(BaseBackend):

    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.filter(email=email).first()
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SettingsBackend(BaseBackend):
    """Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.
    Use the login name and a hash of the password."""

    def authenticate(self, request, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
