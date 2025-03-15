from functools import lru_cache

from django import forms
from django.contrib.auth.hashers import make_password
from rest_framework import status
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from models.models.users.models import User


class RegisterUserService(ServiceWithResult):
    username = forms.CharField(max_length=127)
    password = forms.CharField(max_length=127)

    custom_validations = ['_validate_username']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._create_user()
        return self
    
    def _create_user(self) -> User:
        return User.objects.create(
            username=self.cleaned_data['username'],
            password=make_password(self.cleaned_data['password'])
        )
    
    @property
    def _user(self) -> User | None:
        return User.objects.filter(username=self.cleaned_data['username']).first()

    def _validate_username(self) -> None:
        if self._user:
            self.add_error(
                field='username',
                error=ValidationError(
                    message=f'Имя {self.cleaned_data["username"]} занято.'
                )
            )
            self.response_status = status.HTTP_400_BAD_REQUEST
         