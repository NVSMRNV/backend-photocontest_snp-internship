from django import forms
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound

from models.models.users.models import User


class UpdatePatchUserService(ServiceWithResult):
    id = forms.IntegerField()
    username = forms.CharField(max_length=127, required=False)
    bio = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    profile_photo = forms.ImageField(required=False)
    custom_validations = ['_validate_user_id']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.user = self._get_user_by_id()
            self.result = self._update_user() 
        return self

    def _update_user(self):
        self.user.username = self.cleaned_data.get('username', self.user.username)
        self.user.bio = self.cleaned_data.get('bio', self.user.bio)
        self.user.email = self.cleaned_data.get('email', self.user.email)
        self.user.profile_photo = self.cleaned_data.get('profile_photo', self.user.profile_photo)
        self.user.save()

        return self.user

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


class UpdatePutUserService(ServiceWithResult):
    id = forms.IntegerField()
    username = forms.CharField(max_length=127, required=False)
    bio = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    profile_photo = forms.ImageField(required=False)
    custom_validations = ['_validate_user_id']

    def process(self):
        self.run_custom_validations()

        if self.is_valid():
            self.user = self._get_user_by_id()
            self.result = self._update_user() 
        return self

    def _update_user(self):
        self.user.username = self.cleaned_data.get('username', '')
        self.user.bio = self.cleaned_data.get('bio', '')
        self.user.email = self.cleaned_data.get('email', '')
        self.user.profile_photo = self.cleaned_data.get('profile_photo', '')
        self.user.save()

        return self.user

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


    