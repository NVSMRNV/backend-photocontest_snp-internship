from django import forms
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound

from models.models.users.models import User


class DeleteUserService(ServiceWithResult):
    id = forms.IntegerField()
    custom_validations = ['_validate_user_id']

    def process(self) -> ServiceWithResult:
        self.run_custom_validations()

        if self.is_valid():
            self.user = self._get_user_by_id()
            self._delete_user(self.user)
        return self
    
    def _delete_user(self, user: User) -> None:
        user.delete()
        self.response_status = status.HTTP_204_NO_CONTENT 

    def _get_user_by_id(self) -> User:
        try:
            return User.objects.get(id=self.cleaned_data['id'])
        except ObjectDoesNotExist:
            return None
        
    def _validate_user_id(self) -> None:
        if not self._get_user_by_id():
            self.add_error(
                'id',
                NotFound(
                    message=f'Пользователь с id: {self.cleaned_data['id']} не найден.'
                )
            )
            self.response_status = status.HTTP_404_NOT_FOUND
