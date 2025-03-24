from functools import lru_cache

from django import forms
from rest_framework import status
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models.models.users.models import User


class DeleteUserService(ServiceWithResult):
    id = forms.IntegerField(min_value=1)

    custom_validations = ['_validate_user_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self._user.delete()
            self.response_status = status.HTTP_200_OK
        return self

    @property
    @lru_cache
    def _user(self) -> User | None:
        return User.objects.filter(id=self.cleaned_data['id']).first()

    def _validate_user_id(self) -> None:
        if not self._user:
            self.add_error(
                field='id',
                error=NotFound(
                    message=f'Пользователь с id = {self.cleaned_data['id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
