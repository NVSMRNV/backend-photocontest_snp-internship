from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.users.models import User


class UpdateUserService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)
    username = forms.CharField(max_length=127, required=False)
    bio = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    profile_photo = forms.ImageField(required=False)
    
    custom_validations = ['_validate_user_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self._update_user()
        return self

    @property
    @lru_cache
    def _user(self):
        return User.objects.filter(id=self.cleaned_data['id']).first()

    def _update_user(self) -> User:
        pass

    def _validate_user_id(self) -> None:
        if not self._user:
            self.add_error(
                field='id',
                error=NotFound(
                    message=f'Пользователь с id = {self.cleaned_data['id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND


class PartialUpdateUserService(UpdateUserService):
    def _update_user(self) -> User:
        for field in ['username', 'bio', 'email', 'profile_photo']:
            value = self.cleaned_data.get(field)
            if value:
                setattr(self._user, field, value)
        self._user.save()
        return self._user


class FullUpdateUserService(UpdateUserService):
    def _update_user(self):
        for field in ['bio', 'email', 'profile_photo']:
            value = self.cleaned_data.get(field)
            if value:
                setattr(self._user, field, value)
            else:
                setattr(self._user, field, None)
        self._user.save()
        return self._user